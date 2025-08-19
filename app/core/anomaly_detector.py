# app/core/anomaly_detector.py
"""
Simple heuristic anomaly detector as placeholder.
Replace with a proper ML model later.
"""
import time
from app.storage.redis_client import get_redis
from loguru import logger

async def is_suspicious(request_context: dict) -> tuple[bool, dict]:
    """
    Very simple rules:
      - If user-agent missing => suspicious
      - If requests/min from IP > threshold (a higher threshold) => suspicious
    Returns (is_suspicious, info)
    """
    ua = request_context["headers"].get("user-agent", "")
    if not ua or ua.strip() == "":
        return True, {"reason": "empty-user-agent"}

    ip = request_context["ip"]
    now = int(time.time())
    window = 60
    redis = await get_redis()
    if redis:
        key = f"anomaly:reqcount:{ip}:{now//window}"
        count = await redis.incr(key)
        if count == 1:
            await redis.expire(key, window)
        # threshold a bit higher than normal rate limit
        if count > 10 * 60:  # e.g., 600 req/min -> suspicious
            logger.warning(f"High request rate for {ip}: {count}")
            return True, {"reason": "high-rate", "count": count}
    else:
        # if no redis, skip heavy checks
        pass

    return False, {}
