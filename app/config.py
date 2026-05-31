# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Gateway settings
GATEWAY_PORT = int(os.getenv("GATEWAY_PORT", 8000))

# Rate limiting 
DEFAULT_RATE_LIMIT_PER_MIN = int(os.getenv("DEFAULT_RATE_LIMIT_PER_MIN", 120))

# API keys list
API_KEYS = [
    k.strip() for k in os.getenv("API_KEYS", "").split(",") if k.strip()
]

# Redis cache
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# JWT settings
JWT_SECRET = os.getenv("JWT_SECRET", "changeme")  
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")


ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Debug print for config validation (remove in production)
if ENVIRONMENT == "development":
    print(f"[Config] Loaded API Keys: {API_KEYS}")
    print(f"[Config] Redis URL: {REDIS_URL}")
    print(f"[Config] Gateway Port: {GATEWAY_PORT}")
