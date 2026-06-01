# app/utils/logger.py
from loguru import logger
import sys
import os
import time


logger.remove()

LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)

logger.add(sys.stdout, colorize=True, format=LOG_FORMAT, level="DEBUG")

LOG_DIR = os.getenv("LOG_DIR", "logs")
os.makedirs(LOG_DIR, exist_ok=True)
logger.add(
    f"{LOG_DIR}/gateway.log",
    rotation="10 MB",
    retention="7 days",
    compression="zip",
    format=LOG_FORMAT,
    level="INFO",
)

async def log_request(
    method: str,
    path: str = "",
    query: dict = None,
    client: str = None,
    duration: float = None,
    status_code: int = None
):
    message = f"{method} {path or ''} | Query={query or {}} | Client={client or 'unknown'}"
    if duration is not None:
        message += f" | Duration={duration:.4f}s"
    if status_code is not None:
        message += f" | Status={status_code}"
    logger.info(message)

