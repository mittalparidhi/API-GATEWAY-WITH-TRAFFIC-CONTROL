import time
import asyncio
import uvicorn
from fastapi import FastAPI, Request
from app.services.forwarder import forward_request
from app.core.router import dynamic_router
from app.utils.logger import log_request

app = FastAPI(title="Self-Learning API Gateway (Core)", debug=True)


@app.middleware("http")
async def log_middleware(request: Request, call_next):
    start_time = time.perf_counter()

    ctx = {
        "method": request.method,
        "path": request.url.path,
        "query": str(request.url.query),
        "client": request.client.host if request.client else None
    }

    # Log before forwarding
    asyncio.create_task(log_request({**ctx, "stage": "request_received"}))

    try:
        response = await call_next(request)
    except Exception as e:
        # Log exception before raising
        asyncio.create_task(log_request({**ctx, "error": str(e)}))
        raise

    latency_ms = (time.perf_counter() - start_time) * 1000
    ctx.update({
        "status": response.status_code,
        "latency_ms": latency_ms,
        "stage": "response_sent"
    })
    asyncio.create_task(log_request(ctx))

    return response

# Exception handler (after app is defined)
@app.exception_handler(Exception)
async def debug_exception_handler(request: Request, exc: Exception):
    return {"error": str(exc), "path": str(request.url)}

# Include dynamic router
app.include_router(dynamic_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
