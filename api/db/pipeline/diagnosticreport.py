from models.common import FhirBasePatientRequest
from pipeline.utils.base_pipeline import BasePipelineFhir
from pipeline.utils.exception_handler import exhandler
from pipeline.utils.filter import DataFilter
from pipeline.utils.paginate import Pagination


class DiagnosticReportPipeline(BasePipelineFhir):
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
        self.collection = "DiagnosticReport"

    @property
    def run(self):
        return self.get_diagnostic_report(self.req)

    @exhandler
    def get_diagnostic_report(self, req: FhirBasePatientRequest) -> list:
        """
        Get diagnostic report by patient id.

        Args:
            patientId (str): The ID of the patient.
            filter (FilterRequest): The filter request object.

        Returns:
            list[dict[str, str]]: The diagnostic report for the specified patient and filter.
        """
        query = [
            {"$unwind": "$entry"},
            {
                "$project": {
                    "_id": 0,
                    "issued": "$entry.resource.issued",
                    "category": "$entry.resource.category.coding.display",
                    "result": "$entry.resource.presentedForm.data",
                    "encounter": "$entry.resource.encounter.reference",
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
