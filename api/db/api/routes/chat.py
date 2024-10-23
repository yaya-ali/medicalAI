from typing import Dict, List
from fastapi import APIRouter, Depends, HTTPException

from auth.src.api.deps import CurrentUser, get_current_user
from models.gennet_types import PatientIdRequired
from models.common import FilterRequest, H2ogptBaseRequest, PaginateRequest
from models.schema import AllChatsModel, ChatModel
from pipeline.utils.exception_handler import APIExceptionResponse
from pipeline.utils.runner import PipelineNames, PipelineRunner


router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("/{patientId}", response_model=List[AllChatsModel] | APIExceptionResponse)
def get_all_chats(
    user: CurrentUser,
    patientId: PatientIdRequired,
    filter: FilterRequest = Depends(),
    paginate: PaginateRequest = Depends(),
):
    """Get all patient scope chat"""

    try:
        userId = user.id.__str__()
        res = PipelineRunner(
            pipeline=PipelineNames["Chat"],
            req=H2ogptBaseRequest(
                **paginate.model_dump(),
                userId=userId,
                patientId=patientId,
            ),
            filter=filter,
            func="get_all_chats_metadata",
        ).run()
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__repr__())

    if isinstance(res, APIExceptionResponse):
        raise HTTPException(status_code=400, detail=res.dict())
    return res


@router.get("/{chatId}", response_model=ChatModel | APIExceptionResponse)
def get_chat(_: CurrentUser, chatId: str):
    """Get chat by chatId"""

    try:
        res = PipelineRunner(
            pipeline=PipelineNames["Chat"],
            req=H2ogptBaseRequest(chatId=chatId),
        ).run
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__repr__())

    if isinstance(res, APIExceptionResponse):
        raise HTTPException(status_code=400, detail=res.dict())
    return res


@router.delete("/{chatId}", response_model=Dict | APIExceptionResponse)
def delete_chat(chatId: str, user: CurrentUser):
    """Delete chat by chatId"""

    try:
        userId = user.id.__str__()
        res = PipelineRunner(
            pipeline=PipelineNames["Chat"],
            req=H2ogptBaseRequest(userId=userId, chatId=chatId),
            filter=filter,
            func="delete_chat",
        ).run()
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__repr__())

    if isinstance(res, APIExceptionResponse):
        raise HTTPException(status_code=400, detail=res.dict())
    return res
