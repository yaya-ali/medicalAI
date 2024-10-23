import uuid
from pydantic import BaseModel, Field
from typing import Any, Dict, List
from datetime import datetime


class BaseH2ogptModel(BaseModel):
    """
    Base model for the H2OGPT API.

    Attributes:
        metadata (dict): A dictionary containing metadata for the model.
        chat_history (list): A list containing the chat history.
    """

    metadata: dict = {}


class ChatModel(BaseModel):
    """
    Chat model for the H2OGPT API.

    This class represents a chat model for the H2OGPT API. It provides methods to convert chat history
    between different formats and perform operations on the chat model.

    Attributes:
        res (dict): The resource dictionary containing the SHA256 hash and content.
        metadata (dict): The metadata associated with the chat model.
        chat_history (list): The chat history stored as a list of dictionaries.

    """

    h2ogpt_resources: Dict[str, Any] = {
        "pipelines": [],
        "urls": [],
        "medPub": [],
        "audioConsultation": [],
    }
    chat_history: List[Dict[str, str]] = Field(default_factory=list)
    metadata: dict = {}

    def model_post_init(self, __context: Any) -> None:
        if self.metadata == {}:  # new chat object
            self.metadata = {
                "dateCreated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "lastUpdated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "chatId": uuid.uuid4().__str__(),
                "tags": [],
                "title": None,
            }

    def h2ogpt_chat_conversation(self):
        """
        Convert the chat history to H2OGPT chat conversation type.

        This method converts the chat history stored in `self.chat_history` to a list of tuples,
        where each tuple represents a conversation in the H2OGPT chat conversation format.

        Returns:
            list[tuple[str, str]]: The H2OGPT chat conversation.

        Example:
            >>> model = Model()
            >>> model.chat_history = [
            ...     {"instruction": "Hello!", "response": "Hi there!"},
            ...     {"instruction": "How are you?", "response": "I'm good, thanks!"},
            ... ]
            >>> model.h2ogpt_chat_conversation()
            [('Hello!', 'Hi there!'), ('How are you?', "I'm good, thanks!")]

        """
        history = []
        for c in self.chat_history:
            history.append((c["instruction"], c["response"]))

        return history

    def db_chat_conversation(
        self,
        chat_conversation: list[tuple[str, str]],
        refresh: bool = False,
    ):
        """
        Convert H2OGPT chat conversation to chat history compatible with MongoDB.

        Args:
            chat_conversation (list[tuple[str, str]]): The H2OGPT chat conversation to be converted.
            refresh (bool, optional): If set to True, the chat history will be refreshed. Defaults to False.

        Returns:
            list[dict]: The converted chat history as a list of dictionaries, where each dictionary contains an instruction and a response.

        """
        history = []
        for c in chat_conversation:
            history.append({"instruction": c[0], "response": c[1]})

        if refresh:
            self.chat_history = history

        return history

    def tosha256(self, content: Any):
        """
        Convert content to SHA256 hash.

        Args:
            content (str): The content to convert.

        Returns:
            str: The SHA256 hash of the content.

        """
        import hashlib

        result = hashlib.sha256(str(content).encode()).hexdigest()
        return result

    def pipeline_exists(self, sha256: str):
        """
        Check if SHA256 hash is in res.

        Args:
            sha256 (str): The SHA256 hash to check.

        Returns:
            bool: True if the SHA256 hash is in res, False otherwise.

        """

        return sha256 in [
            r["sha256sum"] for r in self.h2ogpt_resources.get("pipelines", [])
        ]

    async def update_tags(self):
        """
        Update the tags in metadata based on the resources present.

        This method checks the h2ogpt_resources field and updates the tags in metadata accordingly.
        If pipelines are present, it appends the pipeline.name to tags.
        If audio is present, it appends the word "audioConsultation" to the tag.
        If medpub is present, it appends the word "medPub" to the tag.
        """

        try:
            if "tags" not in self.metadata:
                self.metadata["tags"] = []

            # Check for pipelines and add their names to tags
            for pipeline in self.h2ogpt_resources.get("pipelines", []):
                if pipeline["name"]:
                    self.metadata["tags"].append(
                        str(pipeline["name"]).replace("Pipeline", "")
                    )

            # Check for audio and add "audioConsultation" to tags
            if self.h2ogpt_resources.get("audioConsultation"):
                self.metadata["tags"].append("audioConsultation")

            # Check for medpub and add "medPub" to tags
            if self.h2ogpt_resources.get("medPub"):
                self.metadata["tags"].append("medPub")

            # Check for urls and add "urls" to tags
            if self.h2ogpt_resources.get("urls"):
                self.metadata["tags"].append("urls")

            # convert tags to set, and back to list to remove duplicates
            self.metadata["tags"] = list(set(self.metadata["tags"]))
            return self.metadata

        except Exception as e:
            raise Exception(f"Something went wrong{e.__str__()}")


class AllChatsModel(BaseH2ogptModel):
    """
    Chat history model for H2OGPT API
    """
