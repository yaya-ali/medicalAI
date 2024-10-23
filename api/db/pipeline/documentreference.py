from models.common import FhirBasePatientRequest
from pipeline.utils.base_pipeline import BasePipelineFhir
from pipeline.utils.exception_handler import exhandler
from pipeline.utils.filter import DataFilter
from pipeline.utils.paginate import Pagination


class DocumentReferencePipeline(BasePipelineFhir):
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
        self.collection = "DocumentReference"

    @property
    def run(self):
        return self.document_reference(req=self.req)

    @exhandler
    def document_reference(self, req: FhirBasePatientRequest) -> list:
        query = [
            {"$unwind": "$entry"},
            {
                "$addFields": {
                    "docContentType": {
                        "$arrayElemAt": [
                            "$entry.resource.content.attachment.contentType",
                            0,
                        ]
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "effectiveDate": "$entry.resource.date",
                    "contentType": "$docContentType",
                    "display": "$entry.resource.type.coding.display",
                    "content": "$entry.resource.content.attachment.data",
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
