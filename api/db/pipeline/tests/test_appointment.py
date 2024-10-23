from pydantic import ValidationError
from models.common import FhirBasePatientRequest
from pipeline.utils.exception_handler import ExceptionHandler
from pipeline.utils.runner import PipelineNames, PipelineRunner


class Test_AppointmentPipeline:
    def test_appointment_runner_should_fail(self):
        try:
            req = FhirBasePatientRequest(fields=[], conditions=[])

            res = PipelineRunner(
                pipeline=PipelineNames["Appointment"],
                req=req,
                **req.model_dump(),
            ).run

            assert res is not None, "Failed to run appointment pipeline"
        # assert len(res) > 0, "Failed to retrieve appointment data"
        except ValidationError:
            ...
        except ExceptionHandler as e:
            assert isinstance(e, ExceptionHandler), "Failed to run appointment pipeline"
            assert (
                "Invalid appointmentId or patientId" in e.msg
            ), "Failed to run appointment pipeline"
