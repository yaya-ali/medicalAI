from models.req import (
    FhirDocumentModelRequest,
    FhirDownloadAttachmentRequest,
)
from pipeline.utils.base_pipeline import BasePipeline
from core.config import settings
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import httpx
import asyncio
from stat import S_ISDIR, S_ISREG
from os.path import join, normpath
import os
import os.path


class ExportUtils(BasePipeline):
    def __init__(self) -> None:
        self.site = settings.FHIR_SITE
        self.url = settings.FHIR_URL
        self.db = settings.FHIR_DB
        self.cursor = self.connection[self.db]
        self.res_dir = settings.FHIR_RES_PATH
        self.threads = []  # type: ignore

    def download_file(self, req: FhirDocumentModelRequest, document_ref: list[dict]):
        """
        Download a file from a URL and save it to a folder
        the folder can be set by the user in .env RES_PATH
        file structure is: {uuid/{category}/{file_name}

        Args:
            req (FhirDocumentModelRequest): request object
            - access_token (str): access token
            - patient_id (str): patient id
            - category (str): category

            document_ref (list[dict]): list of document reference

        Returns:
            None: None
        """
        headers = {
            "Authorization": f"Bearer {req.access_token}",
            "Accept": "*/*",
        }
        # docTitle is the file name
        doc_info_list = [
            (entry["docUrl"], entry["docTitle"], entry["docCategory"])
            for entry in document_ref
        ]

        def fetch_and_write(
            url: str, file_name: str, category: str, client: httpx.Client
        ):
            # if the file exists, don't download it
            if not os.path.isfile(
                os.path.join(
                    os.getcwd(),
                    self.res_dir,
                    req.patient_id,
                    category,
                    file_name,
                )
            ):
                # create the folder if it doesn't exist
                os.makedirs(
                    os.path.join(os.getcwd(), self.res_dir, req.patient_id, category),
                    exist_ok=True,
                )
                with open(
                    os.path.join(
                        os.getcwd(),
                        self.res_dir,
                        req.patient_id,
                        category,
                        file_name,
                    ),
                    "wb",
                ) as file:
                    with client.stream(method="GET", url=url) as res:
                        for chunk in res.iter_bytes():
                            file.write(chunk)

        with httpx.Client(headers=headers) as client:
            [
                fetch_and_write(url, file_name, category, client)
                for url, file_name, category in doc_info_list
            ]

    async def save_bulk_response(
        self,
        endpoints,
        headers,
        db_init: bool = False,
        **kwargs,
    ):
        """
        Save a response from a request to a file
        the folder can be set by the user in .env RES_PATH
        file structure is: {uuid}/{category}/{file_name}

        Args:
            endpoints (list): list of endpoints
            headers (dict): headers
            db_init (bool, optional): save to db. Defaults to False.

        Returns:
            None: None if successful
        """

        patient_id: str = str(kwargs.get("patient_id"))
        category: str = str(kwargs.get("category"))
        binary_folder = os.path.join(os.getcwd(), str(self.res_dir))
        output_directory = os.path.join(binary_folder, patient_id, category)
        os.makedirs(output_directory, exist_ok=True)

        urls = [
            (
                lambda url: f"{url}/apis/{self.site}/fhir/{endpoint}?patient={patient_id}"
            )(self.url)
            for endpoint in endpoints
        ]
        meta = f"{self.url}/apis/{self.site}/fhir/Patient/{patient_id}"
        vitals = f"{self.url}/apis/{self.site}/fhir/Observation?patient={patient_id}&category=vital-signs&code=85353-1"
        urls.append(meta)
        urls.append(vitals)

        async def httpx_fetch(url: str, client: httpx.AsyncClient) -> dict:
            response = await client.get(url, timeout=None)
            return response.json()

        def save_to_mongo(endpoint: str, response: dict | None):
            if response is None:
                return None

            try:
                response["_id"] = patient_id
                self.cursor[endpoint].update_one(
                    {"_id": patient_id}, {"$set": response}, upsert=True
                )

            except Exception as e:
                raise Exception(f"Invalid Request: {e}")

        async with httpx.AsyncClient(headers=headers) as client:
            if db_init:
                task = [httpx_fetch(url, client) for url in urls]
                responses: list[dict | None] = await asyncio.gather(*task)

                with ThreadPoolExecutor() as executor:
                    endpoints.append("Patient")
                    endpoints.append("Vitals")

                    for urlz, endpoint, response in zip(
                        urls,
                        endpoints,
                        responses,
                    ):
                        executor.submit(save_to_mongo, endpoint, response)

                        if (
                            "85353-1" in urlz and db_init
                        ):  # constant code for vitals (fhir)
                            executor.submit(save_to_mongo, "Vitals", response)

            # this is only use for debugging
            self._flush_threads()

    def _flush_threads(self):
        """Flush all threads."""
        for thread in self.threads:
            thread.join()

    def download_attachment(self, req: FhirDownloadAttachmentRequest):
        """
        Downloads an attachment file and returns its file path.

        Args:
            req (DownloadAttachmentRequest): The request object containing the necessary information.

        Returns:
            Path: The file path of the downloaded attachment.

        Raises:
            Exception: If the file is not found.
        """

        base_dir = Path(__file__).parent.parent.parent

        if req.reference_path is not None:
            static_folder = Path(normpath(join(base_dir, "binary", req.reference_path)))

            if not str(static_folder).startswith(str(base_dir)):
                raise Exception("Invalid file path")

            mode = os.lstat(static_folder).st_mode
            if S_ISDIR(mode):
                # It's a directory
                raise Exception("directory given not file!")
            elif S_ISREG(mode):
                # It's a file
                return static_folder
            else:
                raise Exception("File not found!")
