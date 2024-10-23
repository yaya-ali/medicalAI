from models.common import FhirBasePersonRequest
from pipeline.utils.base_pipeline import BasePipelineFhir
from pipeline.utils.filter import DataFilter
from pipeline.utils.paginate import Pagination


class PersonPipeline(BasePipelineFhir):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.req: FhirBasePersonRequest = kwargs.get(
            "req",
            FhirBasePersonRequest(
                _personId=kwargs.get("personId", None),
                fields=[],
                conditions=[],
            ),
        )
        self.collection = "Person"

    @property
    def run(self):
        return self.get_person(self.req)

    def get_person(self, req: FhirBasePersonRequest):
        query = [
            {"$unwind": "$entry"},
            {
                "$project": {
                    "lastUpdated": "$entry.resource.meta.lastUpdated",
                    "personId": "$entry.resource.id",
                    "personName": "$entry.resource.name",
                    "isActive": "$entry.resource.active",
                }
            },
        ]

        if req.personId:
            query.insert(1, {"$match": {"entry.resource.id": req.personId}})

        if req.limit or req.skip:
            query = Pagination().paginate(
                query=query,
                skip=req.skip,
                limit=req.limit,
            )

        result = [result for result in self.cursor[self.collection].aggregate(query)]  # type: ignore[arg-type]

        if req.conditions and req.fields:
            result = DataFilter().filter(
                conditions=req.conditions,
                fields=req.fields,
                data=result,
            )
        return result
