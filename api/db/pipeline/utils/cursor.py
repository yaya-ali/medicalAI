from core.config import settings


class Cursor:
    """init cursor object
    Members:
        user: str | None
        passwd: str | None
        host: str | None
        port: str | None
        connection: MongoClient
    """

    user: str = settings.MONGO_USER
    passwd: str = settings.MONGO_PASS
    host: str = settings.MONGO_HOST
    port: int = settings.MONGO_PORT
