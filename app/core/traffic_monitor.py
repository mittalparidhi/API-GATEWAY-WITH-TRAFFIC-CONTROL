# app/core/traffic_monitor.py
from loguru import logger
import asyncio

# Lightweight asynchronous logger for request metadata.
# In production, you'd push to Kafka/ElasticSearch/Mongo.

async def log_request(ctx: dict):
    """
    ctx: a small dict with fields: timestamp, ip, path, method, status, latency_ms, headers
    """
    # For demo, just write to logger asynchronously
    logger.info(f"[TRAFFIC] {ctx['timestamp']} {ctx['ip']} {ctx['method']} {ctx['path']} status={ctx.get('status')}")
    # optionally, write to a file, DB, or publish to monitoring stream
    await asyncio.sleep(0)  # yield control
