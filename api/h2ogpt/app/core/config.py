from pathlib import Path
from typing import Any, Literal
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_DIR = Path(__file__).parent.parent.parent


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f"{PROJECT_DIR}/.env",
        env_ignore_empty=True,
        extra="ignore",
    )

    # App settings
    API_VERSION_PREFIX: str
    PROJECT_NAME: str
    DOMAIN: str
    VERBOSE: int
    ENVIRONMENT: Literal["local", "staging", "production"]
    BACKEND_CORS_ORIGINS: str

    @computed_field  # type: ignore[misc]
    @property
    def server_host(self) -> str:
        # Use HTTPS for anything other than local development
        if self.ENVIRONMENT == "local":
            return f"http://{self.DOMAIN}"
        return f"https://{self.DOMAIN}"

    # H2ogpt
    H2OGPT_API_URL: str
    H2OGPT_API_KEY: str
    H2OGPT_MAX_WORKERS: int
    H2OGPT_RES_DIR: str
    H2OGPT_AUTH_USER: str
    H2OGPT_AUTH_PASS: str
    H2OGPT_CHUNK_SIZE: int
    H2OGPT_LANGCHAIN_MODE: str
    H2OGPT_LANGCHAIN_ACTION: str


settings = Settings()  # type: ignore
