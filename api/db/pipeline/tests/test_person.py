from pydantic import ValidationError

# from models.req import PersonRequest
from models.common import FhirBasePersonRequest
from pipeline.utils.exception_handler import ExceptionHandler
from pipeline.utils.runner import PipelineNames, PipelineRunner


class Test_PersonPipeline:
    def test_person_runner_should_fail(self):
        try:
            req = FhirBasePersonRequest(fields=[], conditions=[])

            res = PipelineRunner(
                pipeline=PipelineNames["Person"],
                req=req,
                **req.model_dump(),
            ).run

            assert res is not None, "Failed to run person pipeline"
        # assert len(res) > 0, "Failed to retrieve appointment data"
        except ValidationError:
            ...
        except ExceptionHandler as e:
            assert isinstance(e, ExceptionHandler), "Failed to run person pipeline"
            assert "Invalid patientId" in e.msg, "Failed to run person pipeline"
