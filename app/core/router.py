from fastapi import APIRouter, Request
import os
import threading
import time
from app.services.forwarder import forward_request
from app.utils.logger import log_request

ROUTE_CONFIG = "routes.env"  # Or load from DB in real case
ROUTE_REFRESH_INTERVAL = 5   # seconds

dynamic_router = APIRouter()
routes_map = {}

def load_routes():
    """Load routes from routes.env into routes_map."""
    global routes_map
    if not os.path.exists(ROUTE_CONFIG):
        routes_map = {}
        return
    with open(ROUTE_CONFIG) as f:
        lines = f.readlines()
    new_routes = {}
    for line in lines:
        if not line.strip() or line.startswith("#"):
            continue
        try:
            path, backend = line.strip().split("=", 1)
            new_routes[path.strip()] = backend.strip()
        except ValueError:
            continue
    routes_map = new_routes
    print(f"[Router] Routes loaded: {routes_map}")

def watch_routes():
    """Watch the routes.env file for changes and reload dynamically."""
    last_mtime = None
    while True:
        try:
            if os.path.exists(ROUTE_CONFIG):
                mtime = os.path.getmtime(ROUTE_CONFIG)
                if last_mtime != mtime:
                    load_routes()
                    last_mtime = mtime
        except Exception as e:
            print(f"[Router] Watch error: {e}")
        time.sleep(ROUTE_REFRESH_INTERVAL)

# ✅ Load routes initially and start watching in background
load_routes()
threading.Thread(target=watch_routes, daemon=True).start()

# ✅ Root info route (accessible at http://127.0.0.1:8000/)
@dynamic_router.get("/")
async def root_info():
    if routes_map:
        return {
            "message": "API Gateway is running",
            "available_routes": list(routes_map.keys()),
            "note": "Send requests to these paths to be forwarded to their respective backends."
        }
    else:
        return {
            "message": "API Gateway is running, but no routes are currently configured.",
            "note": "Please update routes.env to add route mappings."
        }

# ✅ Catch-all route for dynamic forwarding
@dynamic_router.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"])
async def catch_all(request: Request, full_path: str):
    backend_url = None
    for prefix, backend in routes_map.items():
        if request.url.path.startswith(prefix):
            backend_url = backend
            break

    if not backend_url:
        return {"error": "No backend mapped for this route"}

    # Log request for analytics/debugging
    log_request(request)

    # Forward the request to the mapped backend
    return await forward_request(request, backend_url)
