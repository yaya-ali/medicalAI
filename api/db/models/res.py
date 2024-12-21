from typing import Any, Dict
from pydantic import BaseModel

from models.schema import ChatModel


class ChatResponse(BaseModel):
    chat: Any
    msg: Dict