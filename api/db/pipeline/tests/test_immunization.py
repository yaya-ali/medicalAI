from pydantic import ValidationError
from models.common import (
    FhirBasePatientRequest,
)
from pipeline.utils.exception_handler import ExceptionHandler
from pipeline.utils.runner import PipelineNames, PipelineRunner


class Test_Immunization:
    def test_immunization_runner_should_fail(self):
        try:
            req = FhirBasePatientRequest(fields=[], conditions=[])

            res = PipelineRunner(
                pipeline=PipelineNames["Immunization"],
                req=req,
                **req.model_dump(),
            ).run

            assert res is not None, "Failed to run immunization pipeline"
        # assert len(res) > 0, "Failed to retrieve appointment data"
        except ValidationError:
            ...
        except ExceptionHandler as e:
            assert isinstance(
                e, ExceptionHandler
            ), "Failed to run immunization pipeline"
            assert "Invalid patientId" in e.msg, "Failed to run immunization pipeline"
