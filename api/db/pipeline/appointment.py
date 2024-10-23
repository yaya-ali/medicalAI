from models.common import FhirBasePatientRequest
from pipeline.patient import PatientPipeline
from pipeline.person import PersonPipeline
from pipeline.utils.base_pipeline import BasePipelineFhir
from pipeline.utils.exception_handler import exhandler
from pipeline.utils.filter import DataFilter
from pipeline.utils.paginate import Pagination


class AppointmentPipeline(BasePipelineFhir):
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
        self.collection = "Appointment"

    @property
    def run(self):
        return self.appointment(req=self.req)

    @exhandler
    def appointment(self, req: FhirBasePatientRequest) -> list:
        """Get all appointment for a patient by patient id

        Args:
            req (AppointmentRequest)
            - patientId: str: Patient ID

        Returns:
            list: all appointment for a patient
        """

        query = [
            {"$unwind": "$entry"},
            {
                "$addFields": {
                    "doctorName": {
                        "$arrayElemAt": [
                            "$entry.resource.participant.actor.reference",
                            1,
                        ]
                    },
                    "appointmentDisplay": {
                        "$arrayElemAt": [
                            "$entry.resource.appointmentType.coding.display",
                            0,
                        ]
                    },
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "lastUpdated": "$meta.lastUpdated",
                    "participants": "$entry.resource.participant.actor",
                    "appointmentId": "$entry.resource.id",
                    "appointmentName": "$appointmentDisplay",
                    "doctorName": "$doctorName",
                    "status": "$entry.resource.status",
                    "start": "$entry.resource.start",
                    "end": "$entry.resource.end",
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

        result = [result for result in self.cursor[self.collection].aggregate(query)]  # type: ignore[arg-type]  # type: ignore[arg-type]

        if req.fields and req.conditions:
            result = DataFilter().filter(
                fields=req.fields,
                conditions=req.conditions,
                data=result,
            )

        for r in result:
            r["doctorName"] = PersonPipeline(
                personId=r["doctorName"].split("/")[1]
            ).run[0]["personName"]
            r["patientId"] = r["participants"][0]["reference"].split("/")[1]
            r["patientNames"] = PatientPipeline(patientId=r["patientId"]).run[0][
                "patientNames"
            ]
            del r["participants"]
        return result
