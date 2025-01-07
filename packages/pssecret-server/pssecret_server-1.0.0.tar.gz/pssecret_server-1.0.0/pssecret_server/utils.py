from uuid import uuid4

from cryptography.fernet import Fernet
from redis.asyncio import Redis

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
