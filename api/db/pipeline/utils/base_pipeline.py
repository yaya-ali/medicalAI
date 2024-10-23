from abc import ABC, abstractmethod

from pymongo import MongoClient
from core.config import settings
from pipeline.utils.cursor import Cursor


class BasePipeline(ABC):
    def __init__(self) -> None:
        try:
            self.mongo = Cursor()
            self.connection: MongoClient = MongoClient(
                f"mongodb://{self.mongo.user}:{self.mongo.passwd}@{self.mongo.host}:{self.mongo.port}/?authMechanism=DEFAULT"
            )
        except Exception as e:
            raise Exception(f"Failed to connect to db {repr(e)}")
        # self.db = None
        # self.cursor = self.connection[self.db]


class BasePipelineFhir(BasePipeline):
    def __init__(self) -> None:
        super().__init__()
        self.db = settings.FHIR_DB
        self.cursor = self.connection[self.db]

    @abstractmethod
    def run(self):
        raise NotImplementedError(
            f"Run method for pipeline: {self.__class__.__name__} Not implemented!"
        )


class BasePipelineChat(BasePipeline):
    def __init__(self) -> None:
        super().__init__()
        self.db = settings.CHAT_DB
        self.cursor = self.connection[self.db]

    @property
    @abstractmethod
    def run(self):
        raise NotImplementedError(
            f"Run method for pipeline: {self.__class__.__name__} Not implemented!"
        )
