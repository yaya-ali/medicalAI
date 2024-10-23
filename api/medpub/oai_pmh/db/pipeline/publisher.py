from typing import Any
from db.pipeline.utils.base_pipeline import BasePipelineFhir
from db.pipeline.utils.filter import DataFilter
from db.pipeline.utils.paginate import Pagination
from medpub.oai_pmh.schema.req import AddPublisherRequest, GetPublisherRequest


class PublisherPipeline(BasePipelineFhir):
    def __init__(self, **kwargs):
        self.collection = "MedicalPublication"
        self.req = kwargs.get(
            "req",
            GetPublisherRequest(
                fields=[],
                conditions=[],
            ),
        )

    @property
    def run(self):
        return self.get_publisher(self.req)

    def get_publisher(self, req: GetPublisherRequest) -> list[list[Any]]:
        """
        Get publisher by disease category

        Args:
            disease (str): Disease category
            filter: FilterRequest

        returns:
            list: A list of publishers
        """

        if req.diseases is None:
            query: Any = [
                {"$project": {"_id": 0}},
            ]
            if req.limit or req.skip:
                query = Pagination().paginate(
                    query=query,
                    skip=req.skip,
                    limit=req.limit,
                )
            return [result for result in self.cursor[self.collection].aggregate(query)]

        if isinstance(req.diseases, list):
            result = []
            for d in req.diseases:
                query = [
                    {
                        "$match": {
                            "disease_category": {
                                "$regex": d,
                                "$options": "i",
                            }
                        }
                    },
                    {"$project": {"_id": 0}},
                ]
                if req.limit or req.skip:
                    query = Pagination().paginate(
                        query=query,
                        skip=req.skip,
                        limit=req.limit,
                    )

                result.append(
                    [result for result in self.cursor[self.collection].aggregate(query)]
                )
            if req.conditions and req.fields:
                result = DataFilter().filter(
                    fields=req.fields,
                    conditions=req.conditions,
                    data=result,
                )

            return result

        query = [
            {
                "$match": {
                    "disease_category": {
                        "$regex": req.diseases,
                        "$options": "i",
                    }
                }
            },
            {"$project": {"_id": 0}},
        ]
        if req.limit or req.skip:
            query = Pagination().paginate(
                query=query,
                skip=req.skip,
                limit=req.limit,
            )

        result = [result for result in self.cursor[self.collection].aggregate(query)]
        if req.conditions and req.fields:
            return DataFilter().filter(
                fields=req.fields,
                conditions=req.conditions,
                data=result,
            )

        return result

    async def add_publisher(self, req: AddPublisherRequest) -> dict[str, str]:
        """
        Add a new publisher

        Args:
            req (AddPublisherRequest): An instance of AddPublisherRequest class.
            - publisher (str): Publisher name
            - disease_category (str): Disease category
            - set_code (str): Set code

        returns:
            dict: A dictionary containing the status and message
            - status (str): Status of the request
            - message (str): Message of the request

        Raises:
            HTTPException: If the request is invalid
        """
        data = {
            "publisher": req.publisher_name,
            "disease_category": req.disease_category,
            "set_code": req.set_code,
            "website": req.website,
        }

        try:
            self.cursor[self.collection].update_one(
                {"set_code": req.set_code}, {"$set": data}, upsert=True
            )
            return {
                "status": "success",
                "message": "Successfully added the publisher to the database",
            }
        except Exception:
            raise Exception(
                f"Invalid Request: Publisher with set code {req.set_code} already exists"
            )
