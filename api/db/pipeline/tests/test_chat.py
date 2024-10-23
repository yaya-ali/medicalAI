import uuid

from models.res import ChatResponse
from models.common import H2ogptBaseRequest
from models.schema import ChatModel
from pipeline.utils.exception_handler import (
    ExceptionHandler,
)
from pipeline.utils.runner import PipelineNames, PipelineRunner


class Test_ChatPipeline:
    def test_chat_runner_should_fail(self):
        req = H2ogptBaseRequest()

        try:
            res = PipelineRunner(
                pipeline=PipelineNames["Chat"],
                req=req,
                **req.model_dump(),
            ).run
            assert res, "Failed to run chat pipeline"
        except AssertionError:
            ...
        except ExceptionHandler as e:
            assert isinstance(e, ExceptionHandler), "Failed to run chat pipeline"

    def test_new_chat(self):
        chat = ChatModel()
        chat.metadata["chatId"] = uuid.uuid4().hex
        chat.metadata["userId"] = uuid.uuid4().hex

        res: ChatResponse = PipelineRunner(
            pipeline=PipelineNames["Chat"],
            req=H2ogptBaseRequest(chat=chat),
            func="new_chat",
        ).run()

        assert res, "Failed to create new chat"
        assert res.chat, "Failed to create new chat"

        assert "success" in res.msg["msg"], "Failed to create new chat"

        assert (
            res.chat.metadata["chatId"] == chat.metadata["chatId"]
        ), "Failed to create new chat"
        assert (
            res.chat.metadata["userId"] == chat.metadata["userId"]
        ), "Failed to create new chat"

    def test_get_chat(self):
        chat = ChatModel()
        chat.metadata["chatId"] = uuid.uuid4().hex
        chat.metadata["userId"] = uuid.uuid4().hex

        chat = (
            PipelineRunner(
                pipeline=PipelineNames["Chat"],
                req=H2ogptBaseRequest(chat=chat),
                func="new_chat",
            )
            .run()
            .chat
        )

        res = PipelineRunner(
            pipeline=PipelineNames["Chat"],
            req=H2ogptBaseRequest(chat=chat),
        ).run
        assert res, "Failed to get chat"
        assert res.metadata["chatId"] == chat.metadata["chatId"], "Failed to get chat"
        assert res.metadata["userId"] == chat.metadata["userId"], "Failed to get chat"

    def test_get_chat_should_fail(self):
        chat = ChatModel()
        chat.metadata["chatId"] = uuid.uuid4().hex
        chat.metadata["userId"] = uuid.uuid4().hex

        try:
            PipelineRunner(
                pipeline=PipelineNames["Chat"],
                req=H2ogptBaseRequest(chat=chat),
            ).run
        except Exception as e:
            assert isinstance(e, ExceptionHandler), "Failed to get chat"

    def test_update_chat(self):
        chat = ChatModel()
        chat.metadata["chatId"] = uuid.uuid4().hex
        chat.metadata["userId"] = uuid.uuid4().hex
        chat = (
            PipelineRunner(
                pipeline=PipelineNames["Chat"],
                req=H2ogptBaseRequest(chat=chat),
                func="new_chat",
            )
            .run()
            .chat
        )

        newChat = PipelineRunner(
            pipeline=PipelineNames["Chat"],
            req=H2ogptBaseRequest(chat=chat),
        ).run

        assert newChat, "Invalid object: chat can't be None"
        assert newChat.metadata["chatId"] == chat.metadata["chatId"]
        assert newChat.metadata["userId"] == chat.metadata["userId"]

        newId = uuid.uuid4().hex
        chat.metadata["chatId"] = newId

        res = PipelineRunner(
            pipeline=PipelineNames["Chat"],
            func="update_chat",
            req=H2ogptBaseRequest(chat=chat),
        ).run()

        assert res, "Failed to update chat"
        assert res.chat, "Failed to update chat"
        assert "success" in res.msg["msg"], "Failed to update chat"
        assert res.chat.metadata["chatId"] == newId, "Failed to update chat"

    def test_delete_chat(self):
        chat = ChatModel()
        chat.metadata["chatId"] = uuid.uuid4().hex
        chat.metadata["userId"] = uuid.uuid4().hex
        chat = (
            PipelineRunner(
                pipeline=PipelineNames["Chat"],
                req=H2ogptBaseRequest(chat=chat),
                func="new_chat",
            )
            .run()
            .chat
        )

        res = PipelineRunner(
            pipeline=PipelineNames["Chat"],
            req=H2ogptBaseRequest(
                chatId=chat.metadata["chatId"],
                userId=chat.metadata["userId"],
            ),
            filter=filter,
            func="delete_chat",
        ).run()

        assert res, "Failed to delete chat"
        assert "success" in res["msg"], "Failed to delete chat"
        assert chat.metadata["chatId"] in res["msg"], "Failed to delete chat"

    def test_all_metadata_chat(self):
        chat = ChatModel()
        chat.metadata["chatId"] = uuid.uuid4().hex
        chat.metadata["userId"] = uuid.uuid4().hex
        chat.metadata["patientId"] = uuid.uuid4().hex
        chat = (
            PipelineRunner(
                pipeline=PipelineNames["Chat"],
                req=H2ogptBaseRequest(chat=chat),
                func="new_chat",
            )
            .run()
            .chat
        )

        res = PipelineRunner(
            pipeline=PipelineNames["Chat"],
            req=H2ogptBaseRequest(
                userId=chat.metadata["userId"],
                patientId=chat.metadata["patientId"],
            ),
            func="get_all_chats_metadata",
        ).run()

        assert res, "Failed to get all metadata chat"
        assert len(res) > 0, "Failed to get all metadata chat"
        assert (
            chat.metadata["userId"] == res[0].metadata["userId"]
        ), "Failed to get all metadata chat"
