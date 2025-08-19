import httpx
from fastapi.responses import StreamingResponse

async def forward_request(request, backend_url):
    # Construct target URL
    target_url = backend_url.rstrip("/") + request.url.path
    if request.url.query:
        target_url += f"?{request.url.query}"

    async with httpx.AsyncClient(follow_redirects=True, timeout=30) as client:
        # Copy request headers except hop-by-hop ones
        headers = {k: v for k, v in request.headers.items()
                   if k.lower() not in {"host", "connection", "keep-alive", "proxy-authenticate", "proxy-authorization", "te", "trailers", "transfer-encoding", "upgrade"}}

        # Read body for methods that allow it
        body = await request.body()

        backend_resp = await client.request(
            method=request.method,
            url=target_url,
            headers=headers,
            content=body if body else None
        )

        # Filter and ensure content-type is preserved
        filtered_headers = {k: v for k, v in backend_resp.headers.items()
                            if k.lower() not in {"connection", "keep-alive", "proxy-authenticate", "proxy-authorization", "te", "trailers", "transfer-encoding", "upgrade"}}

        if "content-type" not in {k.lower() for k in filtered_headers}:
            filtered_headers["content-type"] = backend_resp.headers.get("content-type", "application/octet-stream")

        return StreamingResponse(
            backend_resp.aiter_bytes(),
            status_code=backend_resp.status_code,
            headers=filtered_headers
        )
