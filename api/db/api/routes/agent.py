from fastapi import APIRouter, Depends, HTTPException
from auth.src.api.deps import get_current_active_superuser
from core.r4.parser import init
from medpub.doaj.core.doaj_core import DOAJCore


router = APIRouter(dependencies=[Depends(get_current_active_superuser)])


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
