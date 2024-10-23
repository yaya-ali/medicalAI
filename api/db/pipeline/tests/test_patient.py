from models.req import PatientRequest
from pipeline.utils.runner import PipelineNames, PipelineRunner


class Test_PatientPipeline:
    def test_patient_runner(self):
        req = PatientRequest(fields=[], conditions=[])

        res = PipelineRunner(
            pipeline=PipelineNames["Patient"],
            req=req,
            **req.model_dump(),
        ).run

        assert res is not None, "Failed to run patient pipeline"
        # assert len(res) > 0, "Failed to retrieve patient data"
