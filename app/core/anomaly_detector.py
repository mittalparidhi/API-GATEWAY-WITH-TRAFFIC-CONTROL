# app/core/anomaly_detector.py

import time
from app.storage.redis_client import get_redis
from loguru import logger

async def is_suspicious(request_context: dict) -> tuple[bool, dict]:
  
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
       
        if count > 10 * 60: 
            logger.warning(f"High request rate for {ip}: {count}")
            return True, {"reason": "high-rate", "count": count}
    else:
        
        pass

    return False, {}
