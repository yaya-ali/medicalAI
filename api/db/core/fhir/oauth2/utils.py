import pkce
from datetime import datetime
import base64


def state() -> str:
    """
    generate client state for oauth2
    """
    return base64.b64encode(str(datetime.now()).encode()).decode()


def challenge() -> tuple[str, str]:
    """
    generate client challenge for oauth2
    """
    return pkce.generate_pkce_pair()


def method() -> str:
    """
    return client challenge method for oauth2
    """
    return "S256"
