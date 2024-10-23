from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f"{PROJECT_DIR}/.env",
        env_ignore_empty=True,
        extra="ignore",
    )

    # logging
    VERBOSE: int

    # mongo related
    MONGO_HOST: str
    MONGO_PORT: int
    MONGO_USER: str
    MONGO_PASS: str
    FHIR_DB: str
    CHAT_DB: str

    # fhir related
    FHIR_URL: str
    FHIR_SITE: str
    FHIR_CLIENT_ID: str
    FHIR_CLIENT_SECRET: str
    FHIR_CLIENT_NAME: str
    FHIR_SCOPE: str
    FHIR_REDIRECT_URIS: List[str] | str
    FHIR_GRANT_TYPE: str
    FHIR_APPLICATION_TYPE: str
    FHIR_TOKEN_ENDPOINT_AUTH_METHOD: str
    FHIR_POST_LOGOUT_REDIRECT_URIS: List[str] | str
    FHIR_CONTACTS: str
    FHIR_JWKS_URI: str
    FHIR_RES_PATH: str


settings = Settings()  # type: ignore
