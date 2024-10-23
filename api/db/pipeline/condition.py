from typing import Any
from models.common import FhirBasePatientRequest
from pipeline.utils.base_pipeline import BasePipelineFhir
from pipeline.utils.exception_handler import exhandler
from pipeline.utils.filter import DataFilter
from pipeline.utils.paginate import Pagination


class ConditionPipeline(BasePipelineFhir):
    """
    Pipeline for retrieving conditions based on patient ID and filter criteria.
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
        self.collection = "Condition"

    @property
    def run(self):
        return self.get_condition(self.req)

    @exhandler
    def get_condition(self, req: FhirBasePatientRequest) -> list[dict[str, Any]]:
        """
        Get condition by patient id

        Args:
            patientId (str): The ID of the patient.
            filter (FilterRequest): The filter criteria for conditions.

        Returns:
            list[dict[str, Any]]: A list of conditions matching the given patient ID and filter criteria.
        """

        query = [
            {"$unwind": "$entry"},
            {
                "$project": {
                    "_id": 0,
                    "lastUpdated": "$entry.resource.recordedDate",
                    "clinicalStatus": "$entry.resource.clinicalStatus.coding.code",
                    "verificationStatus": "$entry.resource.verificationStatus.coding.code",
                    "category": "$entry.resource.category.coding.code",
                    "conditionCodingName": "$entry.resource.code.text",
                    "encounterReference": "$entry.resource.encounter.reference",
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

        if req.conditions and req.fields:
            result = DataFilter().filter(
                conditions=req.conditions,
                fields=req.fields,
                data=result,
            )

        return result
