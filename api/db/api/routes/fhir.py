from fastapi import APIRouter, Depends, HTTPException, Response
from auth.src.api.deps import CurrentUser
from auth.src.core.config import settings
from core.fhir.oauth2.oauth2 import FhirOauth2
from models.req import (
    FhirAuthorizeRequest,
    FhirRefreshTokenRequest,
    FhirRegistrationRequest,
    FhirTokenRequest,
)

router = APIRouter()


@router.post("/registration")
async def client_register(req: FhirRegistrationRequest, _: CurrentUser):
    """Register new client-app, Users need to login manually and approve the app"""

    try:
        return FhirOauth2().fhir_register(req)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid Request: {e}")


@router.get("/redirect")
def oauth2_redirect(
    response: Response,
    req: FhirTokenRequest = Depends(),
):
    """
    Return `access_token` and `refresh_token` after successful oauth2 authorization
    and set cookie for `access_token` and `refresh_token`
    """

    try:
        result = FhirOauth2().fhir_token(req)
    except HTTPException as e:
        raise e
    try:
        response.set_cookie(
            key="access_token",
            value=result["access_token"],
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )
        response.set_cookie(
            key="refresh_token",
            value=result["refresh_token"],
            max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES,
        )
        return result
    except Exception:
        return result


@router.get("/authorize")
def oauth2_authorize(_: CurrentUser, req: FhirAuthorizeRequest = Depends()):
    """Return oauth2 url to authorize the app"""

    return FhirOauth2().fhir_authorize(req)


@router.post("/oauth2/fhir/refresh_token")
async def refresh_token(_: CurrentUser, req: FhirRefreshTokenRequest = Depends()):
    """
    Refresh access_token by giving refresh_token
    offline_access need to be granted for this route to work
    """

    return FhirOauth2().fhir_refresh_token(req)
