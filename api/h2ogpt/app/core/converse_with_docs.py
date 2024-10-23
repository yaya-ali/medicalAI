from fastapi.responses import StreamingResponse
from db.models.common import FhirBasePatientRequest, H2ogptBaseRequest
from db.pipeline.utils.runner import PipelineNames, PipelineRunner
from h2ogpt.app.schemas.request import (
    BaseConverseRequest,
    ConverseWithDocsRequest,
    H2ogptRequest,
)
from h2ogpt.app.schemas.response import APIExceptionResponse
from h2ogpt.app.core.utils.download_doi import DownloadDOI
from h2ogpt.app.core.utils.download_httpx import HttpxDownloader
from h2ogpt.app.core.utils.exceptions import ExceptionHandler, exhandler
from h2ogpt.app.core.converse import H2ogptConverse
from h2ogpt.app.core.config import settings
from typing import Any

import os


class H2ogptConverseWithDocs(H2ogptConverse):
    """
    supports doi, pipeline, urls, upload

    upload [done]
    doi -- create the entire module, but without the db, only the downloading function. and save it under /tmp/h2ogpt/doi [done]
    pipeline -- create a very simple mongodb pipeline that will stream the data from the db to the model. sample data should be a json containing some info [done]
    urls -- download the urls and save them under /tmp/h2ogpt/urls [done]


    write test for utils classes
        - client [need h2ogpt]
        - exceptions [no need]
        - download_doi [done]
        - upload [need h2ogpt]
        - httpxDownloader [done]


    - chat operational endpoints
    - build converseWithDocs [combine all the above functionalities] [done]


    test converse and converseWithDocs

    - test the following on server with h2ogpt
        - upload [done]
        - doi
        - pipeline [done]
        - urls
        - converse [done]
        - converseWithDocs [done]
    """

    def __init__(self, req: H2ogptRequest) -> None:
        super().__init__(req)

    @exhandler
    async def build_dois(self, req: ConverseWithDocsRequest) -> list:
        dois = []

        for d in req.dois:
            try:
                path = os.path.join(settings.H2OGPT_RES_DIR, f"{self._fname(d)}.pdf")
                from stat import S_ISREG

                mode = os.stat(path).st_mode
                if not S_ISREG(mode):
                    raise FileNotFoundError

                sources = self.sources(refresh=True)
                for src in sources:
                    if f"{self._fname(d)}" in src:
                        dois.append(src)

            except FileNotFoundError:
                return DownloadDOI().download(
                    doi=d,
                    client=self,
                    h2ogpt_path=True,
                )
        return dois

    @exhandler
    async def build_pipelines(
        self, req: ConverseWithDocsRequest
    ) -> list | APIExceptionResponse:
        result = []
        for p in req.pipelines:
            try:
                result.append(
                    PipelineRunner(
                        pipeline=PipelineNames[p],
                        req=FhirBasePatientRequest(
                            fields=req.fields,
                            conditions=req.conditions,
                            patientId=req.patientId,
                        ),
                    ).run
                )

                if not self.chat.pipeline_exists(self.chat.tosha256(str(result))):
                    self.chat.h2ogpt_resources["pipelines"].append(
                        {
                            "sha256sum": self.chat.tosha256(str(result)),
                            "content": result,
                            "name": PipelineNames[p].value,
                        }
                    )
            except Exception as e:
                raise ExceptionHandler(
                    exception=e,
                    msg="Unsupported pipeline name",
                    solution="Check the pipeline names and try again.",
                )

        return result

    @exhandler
    async def build_urls(self, req: ConverseWithDocsRequest) -> list:
        urls = []

        # TODO: validator for all converse.* members
        for u in req.urls:
            try:
                path = os.path.join(settings.H2OGPT_RES_DIR, f"{self._fname(u)}.pdf")
                from stat import S_ISREG

                mode = os.stat(path).st_mode
                if not S_ISREG(mode):
                    raise FileNotFoundError

                urls.append(path)

            except FileNotFoundError:
                urls.append(
                    HttpxDownloader().download_simple(
                        url=u,
                        dest=os.path.join(settings.H2OGPT_RES_DIR, u),
                    )
                )

        self.sources(refresh=True)
        return urls

    # TODO: this should be same as production, in-fact this need to be rewritten
    @exhandler
    async def load_context(
        self, req: ConverseWithDocsRequest, document_choice: list[str]
    ):
        # If there's no chat res and no document choice, start a new conversation
        # we dont need this

        if not self.chat.h2ogpt_resources["pipelines"] and len(document_choice) == 0:
            return await self.converse(
                BaseConverseRequest(
                    chatId=req.chatId,
                    instruction=req.instruction,
                    patientId=req.patientId,
                )
            )

        # If there's no res, return the instruction from the request.
        if not self.chat.h2ogpt_resources["pipelines"]:
            return req.instruction
        else:
            context = "\n".join(
                str(x["content"]) for x in self.chat.h2ogpt_resources["pipelines"]
            )
            return {
                "user_paste": self.paste(context),
                "instruction": req.instruction,
            }

    def _fname(self, s: str) -> str:
        return f"{s.replace('/', '_')}"

    @exhandler
    async def instruction_send(
        self, req: ConverseWithDocsRequest, document_choice: list[str]
    ) -> StreamingResponse | APIExceptionResponse:
        """
        Send instruction with document_choice to the model and return the response.
        """
        user_paste = None
        instruction = await self.load_context(req, document_choice)

        # if the theres no context and no file given
        # then we will just send the instruction and get the result
        if isinstance(instruction, StreamingResponse):
            return instruction

        if isinstance(instruction, APIExceptionResponse):
            return APIExceptionResponse(
                **instruction.dict(),
            )

        if isinstance(instruction, dict):
            user_paste = instruction["user_paste"]
            document_choice.append(user_paste)
            instruction = instruction["instruction"]

        kwargs = dict(
            instruction=instruction,
            langchain_mode=self.langchain_mode,
            langchain_action=req.langchain_action,
            stream_output=False,
            h2ogpt_key=self.h2ogpt_key,
            top_k_docs=req.top_k_docs,  # -1 entire doc
            document_subset="Relevant",
            document_choice=document_choice,
            chat_conversation=self.chat_conversation,
            do_sample=False,
        )

        job = self.client.submit(
            kwargs,
            api_name="/submit_nochat_api",
        )

        async def generate():
            response = ""
            async for r in self.stream(job):
                yield r
                response += r

            self.chat_conversation.append((req.instruction, response))
            self.chat.db_chat_conversation(
                chat_conversation=self.chat_conversation, refresh=True
            )

            # TODO: run on a separate thread
            await self.gen_title()
            await self.chat.update_tags()
            PipelineRunner(
                pipeline=PipelineNames["Chat"],
                func="update_chat",
                req=H2ogptBaseRequest(chat=self.chat),
            ).run()

            if user_paste:  # clear clipboard
                self.delete_sources(user_paste)

        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={"x-gennet-chatid": self.chat.metadata["chatId"]},
        )

    @exhandler
    async def converse_with_docs(self, req: ConverseWithDocsRequest) -> Any:
        document_choice = []

        if req.dois:
            document_choice.append(await self.build_dois(req))

        if req.pipelines:
            await self.build_pipelines(req)

        if req.urls:
            document_choice.append(await self.build_urls(req))

        if req.h2ogpt_path:
            document_choice.append(*req.h2ogpt_path)

        return await self.instruction_send(req, document_choice)
