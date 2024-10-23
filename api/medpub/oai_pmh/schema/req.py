from datetime import date
from typing import List, Optional
from pydantic import BaseModel
from db.models.common import FilterRequest, PaginateRequest


class InitMedicalPublicationRequest(BaseModel):
    url: str
    meta_prefix: str
    verb: str
    start: date
    end: Optional[date] = None


class AddPublisherRequest(BaseModel):
    disease_category: str
    publisher_name: str
    website: str
    set_code: str


class GetPublisherRequest(FilterRequest, PaginateRequest):
    diseases: Optional[List[str]] = None


class GetPublicationRequest(FilterRequest, PaginateRequest):
    diseases: Optional[List[str]] = None
