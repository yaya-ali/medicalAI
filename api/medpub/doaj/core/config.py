from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f"{PROJECT_DIR}/.env",
        env_ignore_empty=True,
        extra="ignore",
    )

    DOAJ_API_URL: str
    DOAJ_API_KEY: str
    DOAJ_ARTICLE_DIR: str = "binary/doaj_articles"
    DOAJ_API_PAGE_SIZE: int = 30
    DOAJ_API_PAGE: int = 1
    DOAJ_API_DISEASES: list = [
        "Heart Disease",
        "Diabetes",
        "Obesity",
        "Cancer",
        "Chronic Respiratory Diseases",
    ]


settings = Settings()  # type: ignore
