from models.common import FhirBasePatientRequest
from pipeline.utils.base_pipeline import BasePipelineFhir
from pipeline.utils.exception_handler import exhandler
from pipeline.utils.filter import DataFilter
from pipeline.utils.paginate import Pagination


class EncounterPipeline(BasePipelineFhir):
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
        self.collection = "Encounter"

    @property
    def run(self):
        return self.get_encounter(self.req)

    @exhandler
    def get_encounter(self, req: FhirBasePatientRequest) -> list:
        """get all encounter for a patient by patient id

        Args:
            req (EncounterRequest)
            - patientId: str: Patient ID

        Returns:
            list: all encounter for a patient
        """
        query = [
            {"$unwind": "$entry"},
            {
                "$addFields": {
                    "lastUpdated": "$entry.resource.meta.lastUpdated",
                    "encounterStatus": "$entry.resource.status",
                    "encounterClassDisplay": {
                        "$arrayElemAt": [
                            "$entry.resource.type.coding.display",
                            0,
                        ]
                    },
                    "encounterDate": "$entry.resource.period.start",
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "lastUpdated": "$lastUpdated",
                    "encounterStatus": "$encounterStatus",
                    "encounterClassDisplay": {
                        "$arrayElemAt": ["$encounterClassDisplay", 0]
                    },
                    "encounterDate": "$encounterDate",
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
