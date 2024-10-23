from typing import Any, Dict, List
from fastapi import APIRouter, Depends, HTTPException, Query
from db.models.common import FilterRequest, PaginateRequest
from db.pipeline.utils.exception_handler import APIExceptionResponse
from medpub.doaj.db.pipeline.articles import DOAJArticlesPipeline
from medpub.doaj.schema.req import DOAJArticleRequest


router = APIRouter()


@router.get("/", response_model=List[Dict[str, Any]] | APIExceptionResponse)
def publication(
    diseases: list[str] = Query(None),
    filter: FilterRequest = Depends(),
    paginate: PaginateRequest = Depends(),
):
    """Get latest medical publication metadata given disease name(s)"""

    try:
        req = DOAJArticleRequest(diseases=diseases)
        res = DOAJArticlesPipeline().article(
            req=req,
            filter=filter,
            paginate=paginate,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__repr__())

    if isinstance(res, APIExceptionResponse):
        raise HTTPException(status_code=400, detail=res.dict())

    return res
