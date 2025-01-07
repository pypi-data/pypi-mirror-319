from typing import Annotated

from cryptography.fernet import Fernet
from fastapi import Depends, FastAPI
from fastapi.exceptions import HTTPException
from redis.asyncio import Redis

from pssecret_server.fernet import get_fernet
from pssecret_server.models import Secret, SecretSaveResult
from pssecret_server.redis_db import get_redis
from pssecret_server.utils import decrypt_secret, encrypt_secret, save_secret

app = FastAPI()

RedisDep = Annotated[Redis, Depends(get_redis)]
FernetDep = Annotated[Fernet, Depends(get_fernet)]


@app.post(
    "/secret",
    summary="Store secret",
    description=(
        "Submit secret, it is saved on the server, get retrieval key in response. "
        "Use that key to retrieve your data. Key could be used only once, "
        "so use it wisely"
    ),
    response_model=SecretSaveResult,
)
async def set_secret(
    data: Secret, redis: RedisDep, fernet: FernetDep
) -> dict[str, str]:
    data = encrypt_secret(data, fernet)
    return {
        "key": await save_secret(data, redis),
    }


@app.get(
    "/secret/{secret_key}",
    summary="Retrieve secret",
    description=(
        "Returns previously saved data if it is still on the server. "
        "Could be the other way around in two cases: "
        "either it has already been retrieved, either storage timeout has expired"
    ),
    response_model=Secret,
    responses={404: {"description": "The item was not found"}},
)
async def get_secret(
    secret_key: str, redis: RedisDep, fernet: FernetDep
) -> dict[str, bytes]:
    data: bytes | None = await redis.getdel(secret_key)

    if data is None:
        raise HTTPException(404)

    return {
        "data": decrypt_secret(data, fernet),
    }
