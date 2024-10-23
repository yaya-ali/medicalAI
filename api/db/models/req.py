import os
from typing import Optional
from fastapi import Query
from pydantic import BaseModel, Field
from models.common import H2ogptBaseRequest, FhirBasePatientRequest
from models.gennet_types import PatientIdOptional, PatientIdRequired


class PatientRequest(FhirBasePatientRequest):
    patientId: PatientIdOptional = Query(None, description="patientId")


class FhirAPIRequest(FhirBasePatientRequest):
    patientId: PatientIdRequired = Query(description="patientId")


class FhirDocumentModelRequest(BaseModel):
    access_token: str
    patient_id: str
    category: str | None = None


class FhirDownloadAttachmentRequest(BaseModel):
    reference_path: str | None = Field(
        default=None,
        alias="reference_path",
        description="Document Reference Path",
    )
    doi: str | None = Field(default=None, alias="doi", description="Document ID")


class FhirClientExportRequest(BaseModel):
    access_token: str
    patient_id: str


class FhirInitMongoRequest(BaseModel):
    access_token: str
    export: Optional[bool] = False
    bulk: Optional[bool] = False
    attachment: Optional[bool] = False
    patient_id: str | None
    system: Optional[bool] = False


class FhirAuthorizeRequest(BaseModel):
    client_id: str | None = Field(
        default=os.getenv("FHIR_CLIENT_ID"), alias="client_id"
    )
    client_secret: str | None = Field(
        default=os.getenv("FHIR_CLIENT_SECRET"), alias="client_secret"
    )
    scope: str | None = Field(default=os.getenv("FHIR_SCOPE"), alias="scope")
    redirect_uri: str | None = Field(
        default=os.getenv("FHIR_REDIRECT_URI"), alias="redirect_uri"
    )
    grant_type: str | None = Field(
        default=os.getenv("FHIR_GRANT_TYPE"), alias="grant_type"
    )


class FhirRegistrationRequest(BaseModel):
    application_type: str | None = Field(
        default=os.getenv("FHIR_APPLICATION_TYPE") or "private",
        alias="application_type",
    )

    redirect_uris: list[str] | None = Field(
        default=os.getenv("FHIR_REDIRECT_URIS")
        or ["https://localhost:8000/api/v1/oauth2/fhir/redirect"],
        alias="redirect_uris",
    )

    post_logout_redirect_uris: list[str] | None = Field(
        default=os.getenv("FHIR_POST_LOGOUT_REDIRECT_URIS")
        or ["https://client.example.org/logout/callback"],
        alias="post_logout_redirect_uris",
    )

    client_name: str | None = Field(
        default=os.getenv("FHIR_CLIENT_NAME") or "gennetai",
        alias="client_name",
    )

    token_endpoint_auth_method: str | None = Field(
        default=os.getenv("FHIR_TOKEN_ENDPOINT_AUTH_METHOD") or "client_secret_post",
        alias="token_endpoint_auth_method",
    )

    contacts: list[str] | None = Field(
        default=os.getenv("FHIR_CONTACTS") or ["0000100100010"],
        alias="contacts",
    )

    scope: str | None = Field(default=os.getenv("SCOPE") or "", alias="scope")

    jwks_uri: str | None = Field(
        default=os.getenv("FHIR_JWKS_URI")
        or "https://localhost:9300/oauth2/default/jwks",
        alias="jwks_uri",
    )

    # TODO: create jwks route
    jwks: dict | None = Field(
        default={
            "keys": [
                {
                    "kty": "RSA",
                    "n": "sl_MjMGRc0uAv09RAZkZRe829cYb56iameyl-m0ArwClJih875bDoEJQnkNcCeX8zNfF2vOvLC8mjsw_mvfAXq_WAjTHGtmQUqltYcLHxT46oxTXAOtQiGqJ6C4qFEx9_HD6OLxogYxPvuKOHCGyUOM5KuovQlGZnWAPttIGxm50IKVEYyICy0ZWALHIMg8q4CPdYS7zoj0BtKZz86zsswUFvblaQr0syD05AnWx5nzFLASHRyHtABjT9woEP3tubCeUhe3oVwDPuaxfnBbiy2vpM7oVlyQc-nDsrvgvm94JDB588XyWFHfJ5JXf4TAXXIi4VNAMWqIDeOnPz97J6w",
                    "e": "AQAB",
                    "use": "sig",
                }
            ]
        },
        alias="jwks",
    )


class FhirTokenRequest(BaseModel):
    grant_type: str | None = Field(
        default=os.getenv("FHIR_GRANT_TYPE"), alias="grant_type"
    )
    redirect_uri: str | None = Field(
        default=os.getenv("FHIR_REDIRECT_URI"), alias="redirect_uri"
    )
    client_id: str | None = Field(
        default=os.getenv("FHIR_CLIENT_ID"), alias="client_id"
    )
    client_secret: str | None = Field(
        default=os.getenv("FHIR_CLIENT_SECRET"), alias="client_secret"
    )
    code: str | None = Field(..., alias="code")


class FhirRefreshTokenRequest(BaseModel):
    refresh_token: str | None = Field(..., alias="refresh_token")
    client_id: str | None = Field(default=os.getenv("CLIENT_ID"), alias="client_id")


class ChatRequest(H2ogptBaseRequest):
    patientId: PatientIdRequired = Query(description="patientId")


class AllChatRequest(BaseModel):
    userId: Optional[str]
