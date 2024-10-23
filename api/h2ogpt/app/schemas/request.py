from typing import List, Optional, Dict
from fastapi import File, Query, UploadFile
from gradio_client import Client
from pydantic import BaseModel, Field
from db.models.common import FilterRequest
from db.models.schema import ChatModel
from db.models.gennet_types import PatientIdOptional, PatientIdRequired
from h2ogpt.app.core.config import settings


class BaseConverseRequest(BaseModel):
    instruction: str = Query(default="Hello there!")
    chatId: Optional[str] = Query(default=None, description="chatId")
    patientId: PatientIdOptional = Query(None, description="patientId")


class ConverseWithDocsRequest(BaseConverseRequest, FilterRequest):
    patientId: PatientIdRequired = Query(..., description="patientId")
    dois: List[str] = Field(default=[])
    pipelines: List[str] = Field(default=[])
    urls: List[str] = Field(default=[])
    h2ogpt_path: List[str] = Field(default=[])
    _langchain_action: str = "Query"
    _top_k_docs: int = -1 if "prod" in settings.ENVIRONMENT else 5

    @property
    def langchain_action(self):
        return self._langchain_action

    @property
    def top_k_docs(self):
        return self._top_k_docs


class SummarizeRequest(BaseModel):
    h2ogpt_path: str = Query(..., description="H2ogpt path return from /upload")
    patientId: PatientIdRequired = Query(..., description="patientId")
    chatId: Optional[str] = Query(default=None, description="chatId")


class DocumentUploadRequest(BaseModel):
    file: UploadFile = File(...)
    _chunk_size: int = 8192

    @property
    def chunk_size(self):
        return self._chunk_size

    @chunk_size.setter
    def chunk_size(self, value):
        self._chunk_size = value


class ChatRequest(BaseModel):
    chat: ChatModel
    chatId: Optional[str]


class ChatResponse(BaseModel):
    chat: ChatModel
    msg: Dict


class PaginateRequest(BaseModel):
    skip: Optional[int] = Query(default=0)  # its like an array, we start from 0
    limit: Optional[int] = Query(default=5)


class DeleteChatRequest(BaseModel):
    chatId: str


class H2ogptRequest(BaseModel):
    client: Client
    userId: str
    req: BaseConverseRequest | ConverseWithDocsRequest | SummarizeRequest

    class Config:  # allow passing Gradio-Client reference
        arbitrary_types_allowed = True
