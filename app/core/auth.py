# app/core/auth.py
from typing import Dict
from app.config import API_KEYS, JWT_SECRET, JWT_ALGORITHM
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from loguru import logger
import hmac

def normalize_headers(headers: Dict[str, str]) -> Dict[str, str]:
    
    return {k.lower(): v for k, v in headers.items()}

def verify_api_key(headers: Dict[str, str]) -> bool:
    
    headers = normalize_headers(headers)
    api_key = headers.get("x-api-key")
    if not api_key:
        return False
    for valid_key in API_KEYS:
        if hmac.compare_digest(api_key.strip(), valid_key):
            return True
    logger.warning("[Auth] Invalid API key provided.")
    return False

def verify_jwt(headers: Dict[str, str]) -> bool:
    
    headers = normalize_headers(headers)
    auth_header = headers.get("authorization")
    if not auth_header or not auth_header.lower().startswith("bearer "):
        return False

    try:
        token = auth_header.split(" ", 1)[1].strip()
    except IndexError:
        logger.warning("[Auth] Malformed Authorization header.")
        return False

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        
        return True
    except ExpiredSignatureError:
        logger.warning("[Auth] JWT token has expired.")
        return False
    except InvalidTokenError as e:
        logger.warning(f"[Auth] Invalid JWT token: {e}")
        return False
    except Exception as e:
        logger.error(f"[Auth] JWT verification error: {e}")
        return False

def is_authenticated(headers: Dict[str, str]) -> bool:
    
    return verify_api_key(headers) or verify_jwt(headers)
