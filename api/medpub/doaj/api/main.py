from fastapi import APIRouter, Depends
from auth.src.api.deps import get_current_user
from medpub.doaj.api import medpub_doaj

# api_router = APIRouter(dependencies=[Depends(get_current_user)])
api_router = APIRouter(dependencies=[])

api_router.include_router(medpub_doaj.router, prefix="/medpub", tags=["medpub"])

# make sure all db are running # 1. run ablembic upgrade,
