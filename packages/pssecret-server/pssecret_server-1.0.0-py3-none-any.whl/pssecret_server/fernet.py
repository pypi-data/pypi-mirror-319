from typing import Annotated

from cryptography.fernet import Fernet
from fastapi import Depends

from pssecret_server.settings import Settings, get_settings


def get_fernet(settings: Annotated[Settings, Depends(get_settings)]) -> Fernet:
    return Fernet(settings.secrets_encryption_key)
