from typing import Any
from models.common import FhirBasePatientRequest
from pipeline.utils.base_pipeline import BasePipelineFhir
from pipeline.utils.exception_handler import exhandler
from pipeline.utils.filter import DataFilter
from pipeline.utils.paginate import Pagination


class PatientPipeline(BasePipelineFhir):
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
        self.collection = "Patient"

    @property
    def run(self):
        return self.patient(req=self.req)

    @exhandler
    def patient(
        self,
        req: FhirBasePatientRequest,
    ) -> list | Any:  # any this can return exception
        """
        Retrieves patient data based on the provided request.

        Args:
            req (FhirBaseRequest): The request object containing the parameters for the patient query.

        Returns:
            list | dict: The patient data matching the request parameters.
        """
        query = [
            {"$unwind": "$entry"},
            {
                "$project": {
                    "_id": 0,
                    "id": "$_id",
                    "patientNames": {
                        "family": "$entry.resource.name.family",
                        "given": "$entry.resource.name.given",
                    },
                    "dob": "$entry.resource.birthDate",
                    "gender": "$entry.resource.gender",
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

        if req.fields and req.conditions:
            result = DataFilter().filter(
                fields=req.fields,
                conditions=req.conditions,
                data=result,
            )
        return result
