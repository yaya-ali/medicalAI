from medpub.oai_pmh.db.pipeline.publisher import PublisherPipeline
import time
import httpx
import xmltodict

from medpub.oai_pmh.schema.req import GetPublisherRequest, InitMedicalPublicationRequest


class InitMedicalPublicationDb(PublisherPipeline):
    def __init__(self):
        super().__init__()

    async def download_publication_metadata_and_load_to_db(
        self, req: InitMedicalPublicationRequest
    ) -> dict:
        """Download the publication metadata and load it to the database
        Args:
            req (InitMedicalPublicationRequest): An instance of InitMedicalPublicationRequest class.
                - verb (str): verb
                - meta_prefix (str): metadata prefix
                - start (str): start date
                - end (str): end date

        Returns:
            dict: A dictionary containing the time taken and the status of the operation.

        Raises:
            HTTPException: Invalid Request

        Examples:
        {   "url": "https://www.ncbi.nlm.nih.gov/pmc/oai/oai.cgi",
            "meta_prefix": "pmc_fm",
            "verb": "ListRecords",
            "start": "2023-10-31"
        }
        """
        t1 = time.perf_counter()
        set_codes = []

        publishers = self.get_publisher(GetPublisherRequest(fields=[], conditions=[]))
        if not publishers:
            raise Exception("No publishers found")

        for publisher in publishers:
            set_codes.append(publisher["set_code"])  # type: ignore[call-overload]

        urls = [
            f"{req.url}?verb={req.verb}&set={set_code}&metadataPrefix={req.meta_prefix}&from={req.start}&until={req.end or ""}"
            for set_code in set_codes
        ]

        try:
            with httpx.Client() as client:
                responses = [client.get(url=url, timeout=None) for url in urls]
                for response, set_code in zip(responses, set_codes):
                    if response.status_code == 200:
                        data = xmltodict.parse(response.text, dict_constructor=dict)
                        data["_id"] = set_code
                        try:
                            self.cursor["Publication"].update_one(
                                {"_id": set_code}, {"$set": data}, upsert=True
                            )
                        except Exception as e:
                            raise Exception(f"Invalid Request: {e}")
                    else:
                        raise Exception(f"Invalid Request: {response.text}")
        except Exception as e:
            raise Exception(f"Invalid Request: {e}")
        t2 = time.perf_counter()

        return {
            "time": t2 - t1,
            "status": "success",
            "message": "Successfully loaded the publication metadata to the database",
        }
