from typing import Any, List, Optional
import warnings
from fastapi import Query
from pydantic import BaseModel, Field

from models.schema import ChatModel
from pydantic.json_schema import PydanticJsonSchemaWarning


class FilterRequest(BaseModel):
    fields: List[str] = Field(Query([], description="Fields to filter by"))
    conditions: List[str] = Field(Query([], description="regex to run field"))

    # TODO: field(query([])) need custom serializer
    warnings.filterwarnings("ignore", category=PydanticJsonSchemaWarning)


class PaginateRequest(BaseModel):
    skip: Optional[int] = Field(
        default=0,
        description="The number of items to skip at the beginning of the result set",
    )
    limit: Optional[int] = Field(
        default=10,
        description="The maximum number of items to return in the result set",
    )


class FhirBasePatientRequest(FilterRequest, PaginateRequest):
    patientId: Optional[str] = Query(None, description="patientId")

    class Config:
        arbitrary_types_allowed = True


class FhirBasePersonRequest(FilterRequest, PaginateRequest):
    _personId: Optional[str] = None

    @property
    def personId(self):
        return self._personId

    @personId.setter
    def personId(self, value):
        self._personId = value


class H2ogptBaseRequest(PaginateRequest):
    chatId: Optional[str] = Query(None, description="chatId")
    patientId: Optional[str] = Query(None, description="PatientId")
    userId: Optional[str] = None
    # chat: Optional[
    #     ChatModel
    # ] = None  # chat contains all above fields, this is for internal use
    chat: Any = None

    class Config:
        arbitrary_types_allowed = True


class GetChatRequest(PaginateRequest, FilterRequest):
    _userId: Optional[str] = None

    @property
    def userId(self):
        return self._userId

    @userId.setter
    def userId(self, value):
        self._userId = value
