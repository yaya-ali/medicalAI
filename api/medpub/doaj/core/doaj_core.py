import httpx
import asyncio
from typing import Any
from db.pipeline.utils.base_pipeline import BasePipeline

from concurrent.futures import ThreadPoolExecutor
from medpub.doaj.utils.doaj_article_parser import DOAJUtils
from medpub.doaj.core.config import settings


class DOAJCore(DOAJUtils, BasePipeline):
    """
    The DOAJCore class represents the core functionality for interacting with the Directory of Open Access Journals (DOAJ).
    It provides methods for fetching articles and journals related to a given disease and saving them in a MongoDB database.
    """

    def __init__(self) -> None:
        super().__init__()
        self.db = "DOAJ_DB"
        self.cursor = self.connection[self.db]

    async def afetch(self, url: str, client: httpx.AsyncClient) -> dict:
        params = {
            "page": settings.DOAJ_API_PAGE,
            "pageSize": settings.DOAJ_API_PAGE_SIZE,
        }
        response = await client.get(url, timeout=None, params=params)
        return response.json()

    async def init_db(self):
        """
        Initialize MongoDB database by fetching data from the DOAJ API and saving it to the database.

        Returns:
            list[dict | None]: The responses received from the DOAJ API for each disease.

        Raises:
            Exception: If there is an error while saving the data.
        """

        def save_to_mongo(
            disease: str,
            response: list[dict[str, Any]] | str | Any,
        ):
            """
            Save the given response to MongoDB database for the specified disease collection.

            Args:
                disease (str): The name of the disease.
                response (Any): The response data to be saved.

            Raises:
                Exception: If there is an error while saving the data.
            """

            if response is None:
                return None

            try:
                if isinstance(response, list):
                    for r in response:
                        r["metadata"]["disease"] = disease
                        self.cursor["ARTICLES"].update_one(
                            {"metadata.id": r["metadata"]["id"]},
                            {"$set": r},
                            upsert=True,
                        )

            except Exception as e:
                raise Exception(f"Invalid Request: {e!r}")

        def _urls():
            for disease in settings.DOAJ_API_DISEASES:
                yield settings.DOAJ_API_URL + "/articles/" + disease  # type: ignore

        urls = _urls()

        async with httpx.AsyncClient() as client:
            tasks = [self.afetch(url, client) for url in urls]
            responses: list[dict | None] = await asyncio.gather(*tasks)

            with ThreadPoolExecutor() as executor:
                for disease, response in zip(settings.DOAJ_API_DISEASES, responses):
                    executor.submit(
                        save_to_mongo, disease, self.parse_article(response)
                    )

        return {
            "status": "success",
            "detail": "Medical Publication DB initiated",
        }
