from models.common import FhirBasePatientRequest
from pipeline.utils.base_pipeline import BasePipelineFhir
from pipeline.utils.exception_handler import exhandler
from pipeline.utils.filter import DataFilter
from pipeline.utils.paginate import Pagination


class VitalsPipeline(BasePipelineFhir):
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
        self.collection = "Observation"

    @property
    def run(self):
        return self.observation(self.req)

    @exhandler
    def observation(self, req: FhirBasePatientRequest):
        query = [
            {"$unwind": "$entry"},
            {
                "$project": {
                    "_id": 0,
                    "lastUpdated": "$entry.resource.meta.lastUpdated",
                    "effectiveDateTime": "$entry.resource.effectiveDateTime",
                    "display": {
                        "$arrayElemAt": [
                            "$entry.resource.code.coding.display",
                            0,
                        ]
                    },
                    "valueQuantity": "$entry.resource.valueQuantity",
                }
            },
            {
                "$match": {
                    "display": {
                        "$regex": "Heart rate|Respiratory rate|Body Height|Body Weight|BMI"
                    }
                }
            },
        ]

        if req.patientId:
            query.insert(
                0,
                {
                    "$match": {
                        "entry.resource.subject.reference": {
                            "$regex": f".*{req.patientId}.*"
                        }
                    }
                },
            )
        if req.limit or req.skip:
            query = Pagination().paginate(
                query=query,
                skip=req.skip,
                limit=req.limit,
            )

        result = [result for result in self.cursor[self.collection].aggregate(query)]  # type: ignore[arg-type]

        if req.fields and req.conditions:
            result = DataFilter().filter(
                fields=req.fields,
                conditions=req.conditions,
                data=result,
            )

        return result
