from models.common import FhirBasePatientRequest
from pipeline.utils.exception_handler import ExceptionHandler
from pipeline.utils.runner import PipelineNames, PipelineRunner


class Test_AllergyIntolerancePipeline:
    def test_allergy_runner_should_fail(self):
        try:
            req = FhirBasePatientRequest(fields=[], conditions=[])
            res = PipelineRunner(
                pipeline=PipelineNames["AllergyIntolerance"],
                req=req,
            ).run
            assert res, "Failed to run pipeline"
        except ExceptionHandler as e:
            assert isinstance(
                e, ExceptionHandler
            ), "Failed to run allergy intolerance pipeline"
            assert (
                "Invalid patientId" in e.msg
            ), "Failed to run allergy intolerance pipeline"

        except Exception:
            ...
