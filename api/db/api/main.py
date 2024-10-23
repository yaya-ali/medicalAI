from fastapi import APIRouter
from api.routes import chat, patient, fhir, agent

api_router = APIRouter()

api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(patient.router, prefix="/patient", tags=["patient"])
api_router.include_router(fhir.router, prefix="/fhir-oauth2", tags=["fhir"])
api_router.include_router(agent.router, prefix="/agent", tags=["agent"])
