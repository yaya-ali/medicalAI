import ast
import asyncio
from fastapi.responses import StreamingResponse
from db.models.common import H2ogptBaseRequest
from db.models.schema import ChatModel
from db.pipeline.utils.runner import PipelineNames, PipelineRunner
from h2ogpt.app.schemas.request import (
    BaseConverseRequest,
    H2ogptRequest,
    SummarizeRequest,
)
from h2ogpt.app.core.utils.client import H2ogptAuth
from h2ogpt.app.core.utils.exceptions import exhandler
from db.pipeline.chat import ChatPipeline


class H2ogptConverse(H2ogptAuth):
    """
    Class representing the conversation handler for H2OGPT.
    """

    def __init__(self, req: H2ogptRequest) -> None:
        super().__init__()
        self.client = req.client
        self.userId = req.userId
        self.req = req.req

        if not self.req.chatId:
            chat = ChatModel()
            chat.metadata["userId"] = self.userId
            chat.metadata["patientId"] = self.req.patientId
            self.req.chatId = chat.metadata["chatId"]

            # Run pipeline to initiate the chat
            self.chat: ChatModel = (
                PipelineRunner(
                    pipeline=PipelineNames["Chat"],
                    req=H2ogptBaseRequest(chat=chat),
                    func="new_chat",
                )
                .run()  # Ensure .run() is called to execute the pipeline
                .chat
            )

            self.chat_conversation = self.chat.h2ogpt_chat_conversation()
        else:
            chat = ChatModel()
            chat.metadata["chatId"] = self.req.chatId

            self.chat = ChatPipeline()
            self.chat = PipelineRunner(
                pipeline=PipelineNames["Chat"],
                req=H2ogptBaseRequest(chat=chat),
            ).run  # Ensure .run() is called to execute the pipeline

            self.chat_conversation = self.chat.h2ogpt_chat_conversation()

        # Update chat conversation in the database
        self.chat.db_chat_conversation(self.chat_conversation, refresh=True)

    @exhandler
    def summarize(self, req: SummarizeRequest):
        instruction = (
            "Give me detailed summary on what's been discussed in this conversation"
        )

        kwargs = dict(
            instruction=instruction,
            langchain_mode=self.langchain_mode,
            langchain_action=self.langchain_action,
            stream_output=True,
            h2ogpt_key=self.h2ogpt_key,
            top_k_docs=self.top_k_docs,  # -1 entire document
            document_subset=self.document_subset,
            document_choice=[req.h2ogpt_path],
            chat_conversation=self.chat_conversation,
            do_sample=False,
        )

        res = self.client.predict(
            kwargs,
            api_name="/submit_nochat_api",
        )
        response = ast.literal_eval(res)["response"]
        sources = ast.literal_eval(res)["sources"]

        transcription = [
            s["content"] for s in sorted(sources, key=lambda x: x["orig_index"])
        ]

        j_transcription = "".join(transcription)

        # Update the chat object with the summary and transcription
        self.chat.metadata["audioSummary"] = response
        self.chat.metadata["audioTranscription"] = j_transcription

        self.chat.h2ogpt_resources["audioConsultation"].append(req.h2ogpt_path)

        # HACK: Update the title
        asyncio.run(self.gen_title(content=[(instruction, j_transcription)]))
        asyncio.run(self.chat.update_tags())

        # Update the chat using the pipeline
        PipelineRunner(
            pipeline=PipelineNames["Chat"],
            func="update_chat",
            req=H2ogptBaseRequest(chat=self.chat),
        ).run()

        return {
            "transcription": j_transcription,
            "summary": response,
            "chatId": self.chat.metadata["chatId"],
        }

    async def gen_title(self, content: list | None = None):
        return None
        chat_conversation = self.chat_conversation if content is None else content
        kwargs = dict(
            instruction="give me a very short summary on what this conversation is about. Not more than 10 words",
            h2ogpt_key=self.h2ogpt_key,
            chat_conversation=chat_conversation,
        )

        res = self.client.predict(
            kwargs,
            api_name="/submit_nochat_api",
        )

        response = ast.literal_eval(res)["response"]
        self.chat.metadata["title"] = response

    @exhandler
    async def converse(self, req: BaseConverseRequest) -> StreamingResponse:
        """
        Perform a conversation with the H2OGPT model.

        Args:
            req (H2ogptBaseChatRequest): The chat request object.

        Returns:
            ConverseResponse: The response object containing
            the model's response, chat ID, and time taken.
        """

        kwargs = dict(
            instruction=req.instruction,
            h2ogpt_key=self.h2ogpt_key,
            chat_conversation=self.chat_conversation,
        )

        # This is a blocking call
        job = self.client.submit(
            kwargs,
            api_name="/submit_nochat_api",
        )

        async def generate():
            response = ""
            async for r in self.stream(job):
                yield r
                response += r

            # Append conversation to the chat and update the database
            self.chat_conversation.append((req.instruction, response))
            self.chat.db_chat_conversation(
                chat_conversation=self.chat_conversation, refresh=True
            )

            # Run concurrently for updating the title and tags
            await self.gen_title()
            await self.chat.update_tags()

            # Update the chat using the pipeline
            PipelineRunner(
                pipeline=PipelineNames["Chat"],
                func="update_chat",
                req=H2ogptBaseRequest(chat=self.chat),
            ).run()

        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={"x-gennet-chatid": self.chat.metadata["chatId"]},
        )
