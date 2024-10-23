from fastapi import Query
from pydantic import BaseModel


class DOAJArticleRequest(BaseModel):
    diseases: list[str] = Query(None, alias="disease")
