from threading import Thread
from typing import Any, Callable, List
import httpx
from models.common import FhirBasePatientRequest
from models.req import FhirClientExportRequest, FhirDocumentModelRequest
from pipeline.utils.base_pipeline import BasePipeline
from pipeline.utils.runner import PipelineNames, PipelineRunner
from core.config import settings
from core.fhir.parser.thread_runner import FunctionRunnerThread
from core.fhir.parser.utils import ExportUtils


class Export(BasePipeline):
    """
    Export patient data and save it under binary_folder/patient/{uuid}/{patient_name}
    all methods in this class required Authorization header with Bearer token
    see https://www.hl7.org/fhir/http.html for more info.
    """

    def __init__(self, req: FhirClientExportRequest) -> None:
        super().__init__()
        self.patient_id = req.patient_id
        self.access_token = req.access_token
        self.db = settings.FHIR_DB
        self.cursor = self.connection[self.db]
        self.threads: List[Any] = []
        self.site = settings.FHIR_SITE
        self.url = settings.FHIR_URL

    def dump_attachment(
        self,
    ):  # get all downloadable docs for the current patient object (url)
        """
        Get all downloadable docs for the current patient object (url), from mongodb

        Returns: None if successful

        Sample attachment metadata:
        [
            {
                "id": "9ae8c3ce-211f-4803-a1c6-01e83d570f16",
                "docLastUpdate": "2024-01-25T05:16:34+00:00",
                "docCategory": "Communication - Eye",
                "docUrl": "https://localhost:9300/apis/default/fhir/Binary/9b2c883e-5bbb-4ff8-b5af-198181853298",
                "docTitle": "Unique ai EHR extension.pdf",
                "docContentType": "application/pdf"
            }
        ]
        """

        # get all doc ref given patient_id

        doc_ref = PipelineRunner(
            pipeline=PipelineNames["DocumentReference"],
            req=FhirBasePatientRequest(conditions=[], fields=[]),
        ).run

        res = FhirDocumentModelRequest(
            access_token=self.access_token,
            patient_id=self.patient_id,
            category="res",
        )

        return ExportUtils().download_file(res, [x for x in doc_ref])

    async def dump_res(self, db_init: bool = True) -> None:
        """
        Dump user resources to binary folder, and save it in mongodb

        Args:
            db_init (bool, optional): If True, initialize the database. Defaults to False.

        Returns:
            None: None if successful

        Raises:
            Exception: Fhir Server Error
        """
        endpoints: list = [
            "AllergyIntolerance",
            "Appointment",
            "Condition",
            "DiagnosticReport",
            "DocumentReference",
            "Encounter",
            "Goal",
            "Immunization",
            "MedicationRequest",
            "Observation",
            "Procedure",
        ]
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }

        await ExportUtils().save_bulk_response(
            endpoints=endpoints,
            headers=headers,
            db_init=db_init,
            patient_id=self.patient_id,
            category="res",  # const
        )

    def system_res(
        self,
        endpoints: list = [
            "Medication",
            "Person",
        ],
    ):
        """
        Save system level resources to mongodb

        Args:
            endpoints (list, optional): list of system level resources. Defaults to ["Person", "Medication"].

        Returns:
            None: None if successful

        Raises:
            Exception: Fhir Server Error
            Exception: Mongo Error
        """
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }
        urls = [
            (lambda url: f"{url}/apis/{self.site}/fhir/{endpoint}")(self.url)
            for endpoint in endpoints
        ]

        def fetch(
            _: Callable[[Thread], Any],  # current thread object
            client: httpx.Client,
            url: str,
            callback: Callable[..., Any],
            collection: str,
        ):
            response = client.get(url, timeout=None)
            if response.status_code == 200:
                return callback(response.json(), collection)
            else:
                raise Exception(
                    f"Fhir Server Error: {response.status_code} {response.text}"
                )

        def save_to_mongo(data: dict, collection: str):
            data["_id"] = f"system_level_resource_{collection}"  # const
            try:
                self.cursor[collection].update_one(
                    {"_id": data["_id"]}, {"$set": data}, upsert=True
                )
            except Exception as e:
                raise Exception(f"Mongo Error: {e}")

        for urlz, endpoint in zip(urls, endpoints):
            with httpx.Client(headers=headers) as client:
                runner = FunctionRunnerThread(
                    fetch,
                    client,
                    urlz,
                    save_to_mongo,
                    endpoint,
                )
                runner.start()
                self.threads.append(runner)
