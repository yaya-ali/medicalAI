from models.common import FhirBasePatientRequest
from pipeline.utils.base_pipeline import BasePipelineFhir
from pipeline.utils.exception_handler import exhandler
from pipeline.utils.filter import DataFilter
from pipeline.utils.paginate import Pagination


class MedicationRequestPipeline(BasePipelineFhir):
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
        self.collection = "MedicationRequest"

    @property
    def run(self):
        return self.medication_request(req=self.req)

    @exhandler
    def medication_request(self, req: FhirBasePatientRequest) -> list:
        query = [
            {"$unwind": "$entry"},
            {
                "$addFields": {
                    "medicationCategory": {
                        "$arrayElemAt": [
                            "$entry.resource.category.coding.display",
                            0,
                        ]
                    },
                    "medicationStatus": "$entry.resource.status",
                    "medicationIntent": "$entry.resource.intent",
                    "medicationAuthoredOn": "$entry.resource.authoredOn",
                    "medicationDisplay": {
                        "$arrayElemAt": [
                            "$entry.resource.medicationCodeableConcept.coding.display",
                            0,
                        ]
                    },
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "lastUpdated": "$entry.resource.meta.lastUpdated",
                    "medicationDisplay": "$medicationDisplay",
                    "medicationCategory": {"$arrayElemAt": ["$medicationCategory", 0]},
                    "medicationStatus": "$medicationStatus",
                    "medicationIntent": "$medicationIntent",
                    "medicationAuthoredOn": "$medicationAuthoredOn",
                }
            },
        ]
        if req.limit or req.skip:
            query = Pagination().paginate(
                query=query,
                skip=req.skip,
                limit=req.limit,
            )

        if req.patientId:
            query.insert(
                1,
                {
                    "$match": {
                        "entry.resource.subject.reference": {
                            "$regex": f".*{req.patientId}.*"
                        }
                    }
                },
            )

        result = [result for result in self.cursor[self.collection].aggregate(query)]  # type: ignore[arg-type]

        if req.fields and req.conditions:
            result = DataFilter().filter(
                fields=req.fields,
                conditions=req.conditions,
                data=result,
            )

        return result
