from db.models.common import FhirBasePatientRequest

from db.pipeline.utils.runner import PipelineNames, PipelineRunner


class Test_Runner:
    def test_pipeline(self):
        PipelineRunner(
            pipeline=PipelineNames["Patient"],
            req=FhirBasePatientRequest(fields=[], conditions=[]),
        ).run

        # assert isinstance(res, list)
        # assert len(res) > 0
        # assert not isinstance(res, APIExceptionResponse), "Exception something failed"
