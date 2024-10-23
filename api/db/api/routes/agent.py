from fastapi import APIRouter, Depends, HTTPException
from auth.src.api.deps import get_current_active_superuser
from core.fhir.parser.init_db import FhirMongoInit
from core.r4.parser import init
from models.req import FhirInitMongoRequest
from medpub.doaj.core.doaj_core import DOAJCore
from medpub.oai_pmh.db.pipeline.publisher import PublisherPipeline
from medpub.oai_pmh.db.init_db import InitMedicalPublicationDb
from medpub.oai_pmh.schema.req import AddPublisherRequest, InitMedicalPublicationRequest


router = APIRouter(dependencies=[Depends(get_current_active_superuser)])


@router.post("/fhir/init_db")
def init_db_fhir(req: FhirInitMongoRequest):
    """
    Use fhir /Patient endpoint to get patient metadata
    as well as `endpoints` list and save it to mongodb

    Args:
        req (FhirInitMongoRequest): Instance of FhirInitMongoRequest
        - access_token: access token
        - export: export patient data
        - bulk: export all patient data
        - patient_id: patient id
        - attachment: export patient attachment
        - system: export system level data eg [Appointment, Medication]

    Returns:
        list | dict | None: all patients from fhir server

    Raises:
        HTTPException: Invalid Request
    """
    try:
        return FhirMongoInit().fhir_patients(req)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid Request: {e}")


@router.post("/medpub/aoi_pmh/init_db")
async def init_db_medpub(req: InitMedicalPublicationRequest):
    """
    Use PMC API to get publication metadata
    and save it to mongodb

    Args:
        req (InitMedicalPublicationRequest): Instance of InitMedicalPublicationRequest
        - url: PMC API url
        - : metadata prefix
        - verb: verb
        - start: start date
        - end: end date (optional)

    Returns:
        dict: response

    Raises:
        HTTPException: Invalid Request

    """
    try:
        return await InitMedicalPublicationDb().download_publication_metadata_and_load_to_db(
            req
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid Request: {e}")


@router.post("/medpub/aoi_pmh/addPublisher")
async def add_publisher(req: AddPublisherRequest):
    """
    Add a publisher to the database

    Args:
        req (AddPublisherRequest): Instance of AddPublisherRequest
        - set_code: PMC set code
        - publisher_name: publisher name
        - publisher_url: publisher url

    Returns:
        dict: response

    Raises:
        HTTPException: Invalid Request
    """
    try:
        return await PublisherPipeline().add_publisher(req)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid Request: {e}")


@router.post("/medpub/doaj/init_db")
async def doaj_initdb():
    """
    Initialize the DOAJ database.

    This function initializes the DOAJ (Directory of Open Access Journals) database.

    Parameters:
    - _: The current user (User): The user making the request.

    Returns:
    - result (Any): The result of the database initialization.

    Raises:
    - HTTPException: If there is an error during the database initialization.

    """
    try:
        return await DOAJCore().init_db()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid Request: {e}")


@router.post("/init/synthea")
async def init_synthea():
    """
    Initialize Synthea database.
    """
    try:
        init()
        return {"message": "Synthea database initialized successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid Request: {e}")
