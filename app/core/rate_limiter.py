# app/core/rate_limiter.py
import time
from loguru import logger
from typing import Optional

from app.storage.redis_client import get_redis
from app.config import DEFAULT_RATE_LIMIT_PER_MIN

# In-memory fallback counters if Redis not available
_inmemory_counters = {}

async def _redis_increment(key: str, window_seconds: int = 60) -> int:
    """
    Increment a key in Redis (or fallback memory) within a sliding time window.
    """
    r = await get_redis()
    if not r:
        # fallback to in-memory
        now = int(time.time())
        bucket_key = f"{key}:{now // window_seconds}"
        _inmemory_counters.setdefault(bucket_key, 0)
        _inmemory_counters[bucket_key] += 1
        return _inmemory_counters[bucket_key]

    # Use INCR + EXPIRE to implement sliding window bucket in Redis
    count = await r.incr(key)
    if count == 1:
        await r.expire(key, window_seconds)
    return int(count)


async def check_rate_limit(client_id: str, limit_per_min: Optional[int] = None) -> bool:
    """
    Check if the client is allowed under the rate limit.
    :param client_id: Unique identifier (IP or API key)
    :param limit_per_min: Max allowed requests per minute
    :return: True if allowed, False if exceeded
    """
    limit = limit_per_min or DEFAULT_RATE_LIMIT_PER_MIN

    # Current time window (per minute)
    now = int(time.time())
    window = 60
    bucket = f"rate:{client_id}:{now // window}"

    # Increment the request count in Redis or fallback memory
    count = await _redis_increment(bucket, window_seconds=window)

    allowed = count <= limit
    if not allowed:
        logger.debug(f"Rate limit exceeded for {client_id}: {count} > {limit}")

    return allowed
