from pydantic import ValidationError
from models.common import FhirBasePatientRequest

from pipeline.utils.exception_handler import ExceptionHandler
from pipeline.utils.runner import PipelineNames, PipelineRunner


class Test_DiagnosticReport:
    def test_allergy_runner_should_fail(self):
        try:
            req = FhirBasePatientRequest(conditions=[], fields=[])
            res = PipelineRunner(
                pipeline=PipelineNames["AllergyIntolerance"],
                req=req,
                **req.model_dump(),
            ).run
            assert isinstance(res, list), "Failed to run pipeline"
            # assert res, "Failed to run pipeline"

        except ValidationError:
            ...
        except ExceptionHandler as e:
            assert isinstance(
                e, ExceptionHandler
            ), "Failed to run allergy intolerance pipeline"
            assert (
                "Invalid patientId" in e.msg
            ), "Failed to run allergy intolerance pipeline"
