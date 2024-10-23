from typing import Any
from models.common import FhirBasePatientRequest
from pipeline.utils.base_pipeline import BasePipelineFhir
from pipeline.utils.exception_handler import exhandler
from pipeline.utils.filter import DataFilter


class AllergyIntolerancePipeline(BasePipelineFhir):
    """
    AllergyIntolerance pipeline
    """

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
        self.collection = "AllergyIntolerance"

    @property
    def run(self):
        return self.get_allergy_intolerance(self.req)

    @exhandler
    def get_allergy_intolerance(
        self, req: FhirBasePatientRequest
    ) -> list[dict[str, Any]]:
        """
        Get allergy intolerance by patient id
        """

        query = [
            {"$unwind": "$entry"},
            {
                "$project": {
                    "_id": 0,
                    "lastUpdate": "$entry.resource.meta.lastUpdated",
                    "clinicalStatus": "$entry.resource.clinicalStatus.coding.display",
                    "clinicalVerification": "$entry.resource.verificationStatus.coding.display",
                    "category": "$entry.resource.category",
                    "criticality": "$entry.resource.criticality",
                    "display": "$entry.resource.code.coding.display",
                    "reaction": "$entry.resource.reaction",
                }
            },
        ]
        if req.patientId is not None:
            query.insert(0, {"$match": {"_id": req.patientId}})

        result = [result for result in self.cursor[self.collection].aggregate(query)]  # type: ignore[arg-type]

        if req.conditions and req.fields:
            result = DataFilter().filter(
                conditions=req.conditions,
                fields=req.fields,
                data=result,
            )

        return result
