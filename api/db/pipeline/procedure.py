from models.common import FhirBasePatientRequest
from pipeline.utils.base_pipeline import BasePipelineFhir
from pipeline.utils.exception_handler import exhandler
from pipeline.utils.filter import DataFilter
from pipeline.utils.paginate import Pagination


class ProcedurePipeline(BasePipelineFhir):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.req: FhirBasePatientRequest = kwargs.get(
            "req",
            FhirBasePatientRequest(
                patientId=kwargs.get("patientId", None),
                fields=[],
                conditions=[],
            ),
        )
        self.collection = "Condition"

    @property
    def run(self):
        return self.procedure(self.req)

    @exhandler
    def procedure(self, req: FhirBasePatientRequest):
        query = [
            {"$unwind": "$entry"},
            {
                "$project": {
                    "_id": 0,
                    "status": "$entry.resource.status",
                    "performedDateTime": "$entry.resource.performedPeriod",
                    "code": "$entry.resource.code.coding",
                    "encounterReference": "$entry.resource.encounter.reference",
                }
            },
        ]

        if req.patientId:
            query.insert(0, {"$match": {"_id": req.patientId}})

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
