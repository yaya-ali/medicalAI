from enum import Enum
from typing import Optional
from pipeline.allergyintolerance import AllergyIntolerancePipeline
from pipeline.appointment import AppointmentPipeline
from pipeline.chat import ChatPipeline
from pipeline.condition import ConditionPipeline
from pipeline.diagnosticreport import DiagnosticReportPipeline
from pipeline.documentreference import DocumentReferencePipeline
from pipeline.encounter import EncounterPipeline
from pipeline.immunization import ImmunizationPipeline
from pipeline.medicationrequest import MedicationRequestPipeline
from pipeline.observation import ObservationPipeline
from pipeline.patient import PatientPipeline
from pipeline.person import PersonPipeline
from pipeline.procedure import ProcedurePipeline
from pipeline.utils.exception_handler import (
    APIExceptionResponse,
    ExceptionHandler,
)
from pipeline.vitals import VitalsPipeline


class PipelineNames(Enum):
    Patient = "PatientPipeline"
    AllergyIntolerance = "AllergyIntolerancePipeline"
    Appointment = "AppointmentPipeline"
    Chat = "ChatPipeline"
    Condition = "ConditionPipeline"
    DiagnosticReport = "DiagnosticReportPipeline"
    DocumentReference = "DocumentReferencePipeline"
    Encounter = "EncounterPipeline"
    Immunization = "ImmunizationPipeline"
    MedicationRequest = "MedicationRequestPipeline"
    Observation = "ObservationPipeline"
    Person = "PersonPipeline"
    Procedure = "ProcedurePipeline"
    Vitals = "VitalsPipeline"


class PipelineRunner:
    pipelines = {
        PipelineNames.Patient: PatientPipeline,
        PipelineNames.AllergyIntolerance: AllergyIntolerancePipeline,
        PipelineNames.Appointment: AppointmentPipeline,
        PipelineNames.Chat: ChatPipeline,
        PipelineNames.Condition: ConditionPipeline,
        PipelineNames.DiagnosticReport: DiagnosticReportPipeline,
        PipelineNames.DocumentReference: DocumentReferencePipeline,
        PipelineNames.Encounter: EncounterPipeline,
        PipelineNames.Immunization: ImmunizationPipeline,
        PipelineNames.MedicationRequest: MedicationRequestPipeline,
        PipelineNames.Observation: ObservationPipeline,
        PipelineNames.Person: PersonPipeline,
        PipelineNames.Procedure: ProcedurePipeline,
        PipelineNames.Vitals: VitalsPipeline,
    }

    def __init__(
        self,
        pipeline: PipelineNames,
        func: Optional[str] = "run",
        **kwargs,
    ) -> None:
        """Pipeline Runner

        Args:
            pipeline (PipelineNames): name of the pipeline
            func (Optional[str], optional): internal func to run. Defaults to 'run'.

        Raises:
            ValueError: when invalid pipeline name is passed
        """
        if pipeline in self.pipelines:
            self.pipeline = self.pipelines[pipeline](**kwargs)
            self.func = func
        else:
            raise ValueError(f"Invalid pipeline name: {pipeline}")

    @property
    def run(self):
        #  and hasattr(self.pipeline, self.func), the hardest bug to find. avoid using copilot
        try:
            result = getattr(self.pipeline, self.func)  # type: ignore
            if isinstance(result, APIExceptionResponse):
                raise ExceptionHandler(
                    exception=result.error,
                    msg=result.msg,
                    solution=result.solution,
                )
            return result
        except Exception as e:
            raise e
