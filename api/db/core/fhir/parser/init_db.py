import asyncio
from time import perf_counter
from fastapi import HTTPException
import httpx
import json
from models.req import FhirClientExportRequest, FhirInitMongoRequest
from core.fhir.parser.export import Export
from pipeline.utils.cursor import Cursor
from core.config import settings


class FhirMongoInit(Cursor):
    def __init__(self) -> None:
        self.url = settings.FHIR_URL
        self.site = settings.FHIR_SITE

    def fhir_patients(self, req: FhirInitMongoRequest) -> list | dict | None:
        """
        get all patients from fhir server
        if export is set to True, export the patient data to binary folder
        and save it in mongodb as well.

        Args:
            req (FhirInitMongoRequest)
            - access_token: str: access token
            - export: bool: export patient data
            - bulk: bool: export all patient data
            - patient_id: str: patient id
            - attachment: bool: export patient attachment

        Returns:
            list | dict | None: all patients from fhir server

        Raises:
            HTTPException: Invalid Request
        """

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {req.access_token}",
        }

        # TODO: cache the response
        with httpx.Client(headers=headers) as client:
            response = client.get(
                f"{self.url}/apis/{self.site}/fhir/Patient", timeout=None
            )
            if response.status_code == 200:
                return self.patients_meta_parser(json.loads(response.text), req)
            elif response.status_code == 401:
                raise Exception("Fhir Unauthorized: Please check your access token")
            else:
                raise Exception(
                    f"Fhir Server Error: {response.status_code} {response.text}"
                )

    def patients_meta_parser(
        self,
        data: dict,
        req: FhirInitMongoRequest,
    ) -> dict | None:
        """
        parse the patients metadata and save it in mongodb

        Args:
            data (dict): patients metadata
            req (FhirInitMongoRequest)
            - access_token: str: access token
            - export: bool: export patient data
            - bulk: bool: export all patient data
            - patient_id: str: patient id
            - attachment: bool: export patient attachment

        Returns:
            dict | None: patients metadata
        """
        t1 = perf_counter()
        try:
            if req.system:  # save system level resources
                client_req = FhirClientExportRequest(
                    access_token=req.access_token, patient_id=""
                )
                Export(client_req).system_res()

            for entry in data["entry"]:
                id = entry["resource"]["id"]
                client_req = FhirClientExportRequest(
                    access_token=req.access_token, patient_id=id
                )
                exporter = Export(client_req)

                if req.export:
                    if req.bulk:
                        asyncio.run(exporter.dump_res())
                    if req.patient_id == id:
                        asyncio.run(exporter.dump_res())
                if req.attachment:
                    exporter.dump_attachment()

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid Request: {e}")
        t2 = perf_counter()
        return {
            "time": t2 - t1,
            "status": "success",
            "message": "Patients metadata saved successfully",
            "system_resources": req.system,
        }
