# app/config.py
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Gateway settings
GATEWAY_PORT = int(os.getenv("GATEWAY_PORT", 8000))

# Rate limiting (requests per minute, per client)
DEFAULT_RATE_LIMIT_PER_MIN = int(os.getenv("DEFAULT_RATE_LIMIT_PER_MIN", 120))

# API keys list (comma-separated in .env)
API_KEYS = [
    k.strip() for k in os.getenv("API_KEYS", "").split(",") if k.strip()
]

# Redis cache/store URL
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# JWT settings
JWT_SECRET = os.getenv("JWT_SECRET", "changeme")  # Change in production!
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

# Optional: Environment indicator
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Debug print for config validation (remove in production)
if ENVIRONMENT == "development":
    print(f"[Config] Loaded API Keys: {API_KEYS}")
    print(f"[Config] Redis URL: {REDIS_URL}")
    print(f"[Config] Gateway Port: {GATEWAY_PORT}")
