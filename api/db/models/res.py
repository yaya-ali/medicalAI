from typing import Dict
from pydantic import BaseModel

from models.schema import ChatModel


class ChatResponse(BaseModel):
    chat: ChatModel
    msg: Dict
