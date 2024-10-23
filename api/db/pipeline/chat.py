from models.common import FilterRequest, H2ogptBaseRequest
from models.res import ChatResponse
from models.schema import ChatModel, AllChatsModel
from pipeline.utils.base_pipeline import BasePipelineChat
from pipeline.utils.exception_handler import exhandler
from pipeline.utils.filter import DataFilter
from pipeline.utils.paginate import Pagination
from datetime import datetime


class ChatPipeline(BasePipelineChat):
    def __init__(self, **kwargs) -> None:
        super().__init__()

        self.req: H2ogptBaseRequest = kwargs.get("req", H2ogptBaseRequest())
        self.filter: FilterRequest = kwargs.get(
            "filter", FilterRequest(fields=[], conditions=["zzz"])
        )
        self.collection = "GennetChat"

    @property
    def run(self):
        return self.get_chat()

    @exhandler
    def get_chat(self) -> ChatModel:
        """get chat history by chatId

        Args:
            ChatId (str): chatId
            userId (str): userId

        Returns:
            dict: chat history
        """

        if self.req.chatId:
            query = [
                {"$match": {"metadata.chatId": self.req.chatId}},
                {"$project": {"_id": 0}},
            ]
        else:
            query = [
                {"$match": {"metadata.chatId": self.req.chat.metadata["chatId"]}},  # type: ignore
                {"$project": {"_id": 0}},
            ]

        try:
            result = [
                result
                for result in self.cursor[self.collection].aggregate(query)  # type: ignore[arg-type]
            ]

            return ChatModel(**result[0])

        except Exception:
            raise Exception("Failed to get chat: Invalid chatId or userId")

    @exhandler
    def new_chat(self):
        """Create a new chat"""

        assert self.req.chat, "Invalid object: chat can't be None"
        self.cursor[self.collection].insert_one(self.req.chat.model_dump())

        return ChatResponse(chat=self.req.chat, msg={"msg": "success"})

    @exhandler
    def update_chat(self) -> ChatResponse:
        """
        Function to save new and update chat history in db

        Args:
            chat (dict): chat history
            chatId (str): chatId
            userId (str): userId
            patientId (str): patientId

        Returns:
            dict: chatId and message
        """
        assert self.req.chat, "Invalid object: chat can't be None"

        self.req.chat.metadata["lastUpdated"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        self.cursor[self.collection].update_one(
            {"metadata.chatId": self.req.chat.metadata["chatId"]},
            {"$set": self.req.chat.model_dump()},
            upsert=True,
        )

        return ChatResponse(chat=self.get_chat(), msg={"msg": "success"})

    @exhandler
    def get_all_chats_metadata(self) -> list[AllChatsModel]:
        """get all user-scope chats metadata

        Returns:
            dict: chat metadata
        """
        query = [
            {
                "$match": {
                    "metadata.userId": self.req.userId,
                    "metadata.patientId": self.req.patientId,
                }
            },
            {"$sort": {"metadata.lastUpdated": -1}},
            {
                "$project": {
                    "_id": 0,
                    "metadata": "$metadata",
                }
            },
        ]

        if self.req.limit or self.req.skip:
            query = Pagination().paginate(
                query,
                skip=self.req.skip,
                limit=self.req.limit,
            )

        result = [result for result in self.cursor[self.collection].aggregate(query)]  # type: ignore[arg-type]
        if self.filter.conditions and self.filter.fields:
            result = DataFilter().filter(
                fields=self.filter.fields,
                conditions=self.filter.conditions,
                data=result,
            )

        return [AllChatsModel(**chat) for chat in result]

    @exhandler
    def delete_chat(self):
        try:
            result = self.cursor[self.collection].delete_one(
                {
                    "metadata.chatId": self.req.chatId,
                    "metadata.userId": self.req.userId,
                }
            )
            if result.deleted_count == 1:
                return {
                    "msg": f"Chat with chatId {self.req.chatId} deleted successfully."
                }
            else:
                raise Exception(
                    "Chat not found or you don't have permission to delete this chat."
                )
        except Exception as e:
            raise Exception(f"Failed to delete chat: {str(e)}")
