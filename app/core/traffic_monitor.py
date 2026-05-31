# app/core/traffic_monitor.py
from loguru import logger
import asyncio

async def log_request(ctx: dict):
   
    logger.info(f"[TRAFFIC] {ctx['timestamp']} {ctx['ip']} {ctx['method']} {ctx['path']} status={ctx.get('status')}")
   
    await asyncio.sleep(0) 
