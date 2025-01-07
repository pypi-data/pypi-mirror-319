# noinspection PyUnresolvedReferences,PyProtectedMember
from typing import Annotated

from fastapi import Depends
from redis import asyncio as aioredis

from pssecret_server.settings import Settings, get_settings


def get_redis(settings: Annotated[Settings, Depends(get_settings)]) -> aioredis.Redis:
    return aioredis.from_url(str(settings.redis_url))
