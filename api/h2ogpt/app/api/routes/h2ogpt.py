from auth.src.api.deps import CurrentUser, get_current_user
from h2ogpt.app.core.converse_with_docs import H2ogptConverseWithDocs
from fastapi import APIRouter, Depends, HTTPException
from gradio_client import Client
from h2ogpt.app.schemas.response import (
    APIExceptionResponse,
    ConverseResponse,
)
from h2ogpt.app.schemas.request import (
    ConverseWithDocsRequest,
    BaseConverseRequest,
    H2ogptRequest,
    SummarizeRequest,
)
from h2ogpt.app.core.utils.client import h2ogpt_client
from h2ogpt.app.core.converse import H2ogptConverse

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post("/converse")
async def converse(
    user: CurrentUser,
    req: BaseConverseRequest = Depends(),
    client: Client = Depends(h2ogpt_client),
):
    """
    Converse with the H2OGPT model, Only LLM.
    """

    try:
        userId = user.id.__str__()
        result = await H2ogptConverse(
            H2ogptRequest(client=client, req=req, userId=userId),
        ).converse(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__repr__())

    if isinstance(result, APIExceptionResponse):
        raise HTTPException(status_code=400, detail=result.dict())

    return result


@router.post(
    "/converseWithDocs",
    response_model=ConverseResponse | APIExceptionResponse,
)
async def converse_with_docs(
    user: CurrentUser,
    req: ConverseWithDocsRequest = Depends(),
    client: Client = Depends(h2ogpt_client),
):
    """
    Converse with the H2OGPT model, with document support.
    """

    try:
        userId = user.id.__str__()
        result = await H2ogptConverseWithDocs(
            H2ogptRequest(client=client, req=req, userId=userId)
        ).converse_with_docs(req)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=e.__repr__())

    if isinstance(result, APIExceptionResponse):
        raise HTTPException(status_code=400, detail=result.dict())
    return result


@router.post("/summarize")
def summarize_transcribe(
    user: CurrentUser,
    req: SummarizeRequest = Depends(),
    client: Client = Depends(h2ogpt_client),
):
    """Summarize the content of given h2ogpt_path"""

    try:
        userId = user.id.__str__()
        result = H2ogptConverse(
            H2ogptRequest(client=client, req=req, userId=userId)
        ).summarize(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__repr__())

    if isinstance(result, APIExceptionResponse):
        raise HTTPException(status_code=400, detail=result.dict())

    return result
