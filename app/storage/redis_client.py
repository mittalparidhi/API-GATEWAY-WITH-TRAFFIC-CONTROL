# app/storage/redis_client.py
import asyncio
import os
from loguru import logger
from typing import Optional

from redis.asyncio import Redis, from_url

from app.config import REDIS_URL

_redis: Optional[Redis] = None


async def get_redis() -> Optional[Redis]:
    global _redis
    if _redis is None:
        try:
            _redis = from_url(REDIS_URL, decode_responses=True)
            # quick ping
            await _redis.ping()
            logger.info("Connected to Redisat {REDIS_URL} ")
        except Exception as e:
            logger.warning(f"Cannot connect to Redis ({REDIS_URL}): {e}")
            _redis = None
    return _redis
