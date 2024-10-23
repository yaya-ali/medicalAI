from typing import List
from fastapi import APIRouter, Depends, HTTPException
from models.common import (
    FhirBasePatientRequest,
)
from models.req import FhirAPIRequest, PatientRequest
from pipeline.utils.exception_handler import APIExceptionResponse
from pipeline.utils.runner import PipelineNames, PipelineRunner


router = APIRouter()


@router.get("", response_model=List | APIExceptionResponse)
def get_patient(req: PatientRequest = Depends()):
    """Get Patient info"""

    try:
        res = PipelineRunner(
            pipeline=PipelineNames["Patient"],
            req=FhirBasePatientRequest(**req.model_dump()),
        ).run
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__repr__())

    if isinstance(res, APIExceptionResponse):
        raise HTTPException(status_code=400, detail=res.dict())
    return res


@router.get("/appointment", response_model=List | APIExceptionResponse)
def get_patient_appointment(req: FhirAPIRequest = Depends()):
    """Get Patient Appointment info"""

    try:
        res = PipelineRunner(
            pipeline=PipelineNames["Appointment"],
            req=FhirBasePatientRequest(**req.model_dump()),
        ).run
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__repr__())

    if isinstance(res, APIExceptionResponse):
        raise HTTPException(status_code=400, detail=res.dict())
    return res


@router.get("/allergyintolerance", response_model=List | APIExceptionResponse)
def get_patient_allergyintolerance(req: FhirAPIRequest = Depends()):
    """Get Patient AllergyIntolerance info"""

    try:
        res = PipelineRunner(
            pipeline=PipelineNames["AllergyIntolerance"],
            req=FhirBasePatientRequest(**req.model_dump()),
        ).run
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__repr__())

    if isinstance(res, APIExceptionResponse):
        raise HTTPException(status_code=400, detail=res.dict())
    return res


@router.get("/documentreference", response_model=List | APIExceptionResponse)
def get_patient_documentreference(req: FhirAPIRequest = Depends()):
    """Get Patient DocumentReference info"""

    try:
        res = PipelineRunner(
            pipeline=PipelineNames["DocumentReference"],
            req=FhirBasePatientRequest(**req.model_dump()),
        ).run
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__repr__())

    if isinstance(res, APIExceptionResponse):
        raise HTTPException(status_code=400, detail=res.dict())
    return res


@router.get("/encounter", response_model=List | APIExceptionResponse)
def get_patient_encounter(req: FhirAPIRequest = Depends()):
    """Get Patient Encounter info"""

    try:
        res = PipelineRunner(
            pipeline=PipelineNames["Encounter"],
            req=FhirBasePatientRequest(**req.model_dump()),
        ).run
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__repr__())

    if isinstance(res, APIExceptionResponse):
        raise HTTPException(status_code=400, detail=res.dict())
    return res


@router.get("/medicationrequest", response_model=List | APIExceptionResponse)
def get_patient_medicationrequest(req: FhirAPIRequest = Depends()):
    """Get Patient MedicationRequest info"""

    try:
        res = PipelineRunner(
            pipeline=PipelineNames["MedicationRequest"],
            req=FhirBasePatientRequest(**req.model_dump()),
        ).run
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__repr__())

    if isinstance(res, APIExceptionResponse):
        raise HTTPException(status_code=400, detail=res.dict())
    return res


@router.get("/immunization", response_model=List | APIExceptionResponse)
def get_patient_immunization(req: FhirAPIRequest = Depends()):
    """Get Patient Immunization info"""

    try:
        res = PipelineRunner(
            pipeline=PipelineNames["Immunization"],
            req=FhirBasePatientRequest(**req.model_dump()),
        ).run
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__repr__())

    if isinstance(res, APIExceptionResponse):
        raise HTTPException(status_code=400, detail=res.dict())
    return res


@router.get("/condition", response_model=List | APIExceptionResponse)
def get_patient_condition(req: FhirAPIRequest = Depends()):
    """Get Patient Condition info"""

    try:
        res = PipelineRunner(
            pipeline=PipelineNames["Condition"],
            req=FhirBasePatientRequest(**req.model_dump()),
        ).run
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__repr__())

    if isinstance(res, APIExceptionResponse):
        raise HTTPException(status_code=400, detail=res.dict())
    return res


@router.get("/observation", response_model=List | APIExceptionResponse)
def get_patient_observation(req: FhirAPIRequest = Depends()):
    """Get Patient Observation info"""

    try:
        res = PipelineRunner(
            pipeline=PipelineNames["Observation"],
            req=FhirBasePatientRequest(**req.model_dump()),
        ).run
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__repr__())

    if isinstance(res, APIExceptionResponse):
        raise HTTPException(status_code=400, detail=res.dict())
    return res


@router.get("/procedure", response_model=List | APIExceptionResponse)
def get_patient_procedure(req: FhirAPIRequest = Depends()):
    """Get Patient Procedure info"""

    try:
        res = PipelineRunner(
            pipeline=PipelineNames["Procedure"],
            req=FhirBasePatientRequest(**req.model_dump()),
        ).run
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__repr__())

    if isinstance(res, APIExceptionResponse):
        raise HTTPException(status_code=400, detail=res.dict())
    return res


@router.get("/vitals", response_model=List | APIExceptionResponse)
def get_patient_vitals(req: FhirAPIRequest = Depends()):
    """Get Patient Vitals info"""

    try:
        res = PipelineRunner(
            pipeline=PipelineNames["Vitals"],
            req=FhirBasePatientRequest(**req.model_dump()),
        ).run
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__repr__())

    if isinstance(res, APIExceptionResponse):
        raise HTTPException(status_code=400, detail=res.dict())
    return res
