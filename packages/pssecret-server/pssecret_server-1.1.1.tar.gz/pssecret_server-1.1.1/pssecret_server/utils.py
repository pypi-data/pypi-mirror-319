from functools import lru_cache
from uuid import uuid4

from cryptography.fernet import Fernet
from redis.asyncio import Redis
from redis.exceptions import ResponseError
from redis.typing import ResponseT

from pssecret_server.models import Secret


def encrypt_secret(data: Secret, fernet: Fernet) -> Secret:
    encrypted = fernet.encrypt(data.data.encode()).decode()
    return Secret(data=encrypted)


def decrypt_secret(secret: bytes, fernet: Fernet) -> bytes:
    return fernet.decrypt(secret)


async def get_new_key(redis: Redis) -> str:
    """Returns free Redis key"""
    while True:
        new_key = str(uuid4())

        if not await redis.exists(new_key):
            return new_key


async def save_secret(data: Secret, redis: Redis) -> str:
    """Save passed data, returns retrieval key"""
    new_key = await get_new_key(redis)
    await redis.setex(new_key, 60 * 60 * 24, data.data)

    return new_key


@lru_cache
async def _is_getdel_available(redis: Redis) -> bool:
    """Checks the availability of GETDEL command on the Redis server instance

    GETDEL is not available in Redis prior to version 6.2
    """
    try:
        await redis.getdel("test:getdel:availability")
    except ResponseError:
        return False

    return True


async def getdel(redis: Redis, key: str) -> ResponseT:
    """Gets the value of key and deletes the key

    Depending on the capabilities of Redis server this function
    will either call GETDEL command, either first call GETSET with empty string
    and DEL right after that.
    """
    result: ResponseT

    if await _is_getdel_available(redis):
        result = await redis.getdel(key)
    else:
        result = await redis.getset(key, "")
        await redis.delete(key)

    return result
