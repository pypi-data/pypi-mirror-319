import base64
import hashlib
import os
import secrets
from typing import Dict, Optional

from fastapi import Depends, HTTPException, Request, Response, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from dell_unisphere_mock_api.core.config import settings

# Security configuration
security = HTTPBasic()

# Mock user database for testing
MOCK_USERS: Dict[str, Dict[str, str]] = {
    "admin": {
        "username": "admin",
        "role": "admin",
        # For testing, we'll use a simple password comparison
        "password": "Password123!",  # Changed to match tutorial default
    }
}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a stored password."""
    # For testing purposes, we'll do a simple comparison
    # In production, this should use proper password hashing
    return plain_password == hashed_password


def generate_csrf_token() -> str:
    """Generate a CSRF token."""
    return base64.b64encode(os.urandom(32)).decode("utf-8")


async def get_current_user(
    request: Request,
    response: Response,
    credentials: HTTPBasicCredentials = Depends(security),
) -> Dict[str, str]:
    """Validate credentials and return the current user."""
    # Debug logging
    print(f"Request path: {request.url.path}")
    print(f"Request headers: {dict(request.headers)}")

    # Skip X-EMC-REST-CLIENT header check for Swagger UI and its API requests
    is_swagger_request = (
        request.url.path.startswith("/docs")
        or request.url.path.startswith("/openapi.json")
        or request.headers.get("referer", "").endswith("/docs")
    )

    # Check header case-insensitively
    has_emc_header = False
    for header_name, header_value in request.headers.items():
        if header_name.lower() == "x-emc-rest-client" and header_value.lower() == "true":
            has_emc_header = True
            break

    if not is_swagger_request and not has_emc_header:
        print("Missing X-EMC-REST-CLIENT header")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="X-EMC-REST-CLIENT header is required",
            headers={"WWW-Authenticate": "Basic"},
        )

    user = MOCK_USERS.get(credentials.username)
    if not user or not verify_password(credentials.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    # Set cookie for subsequent requests
    response.set_cookie(
        key="mod_sec_emc",
        value=secrets.token_urlsafe(32),
        httponly=True,
        secure=True,
        samesite="lax",  # Added for better security with Swagger UI
    )

    # Only set CSRF token if enabled
    if settings.CSRF_ENABLED:
        csrf_token = generate_csrf_token()
        response.headers["EMC-CSRF-TOKEN"] = csrf_token
        print(f"Generated CSRF token: {csrf_token}")
        print(f"Response headers: {dict(response.headers)}")
        return {
            "username": user["username"],
            "role": user["role"],
            "csrf_token": csrf_token,
        }

    return {
        "username": user["username"],
        "role": user["role"],
    }


def verify_csrf_token(request: Request, method: str) -> None:
    """Verify CSRF token for POST, PATCH and DELETE requests."""
    # Skip CSRF verification if disabled
    if not settings.CSRF_ENABLED:
        return

    print(f"Verifying CSRF token for {method} request to {request.url.path}")
    print(f"Request headers: {dict(request.headers)}")

    if method not in ["POST", "PATCH", "DELETE"]:
        print("Skipping CSRF check - not a POST/PATCH/DELETE request")
        return

    # Skip CSRF check for the auth endpoint
    if request.url.path == "/api/auth":
        print("Skipping CSRF check - auth endpoint")
        return

    # Skip CSRF check only for unauthorized requests to non-GET methods
    if not request.headers.get("Authorization"):
        print("Skipping CSRF check - no Authorization header")
        return

    # Check for CSRF token in both uppercase and lowercase variants
    token = request.headers.get("EMC-CSRF-TOKEN") or request.headers.get("emc-csrf-token")
    if not token:
        print("CSRF token missing from request headers")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="EMC-CSRF-TOKEN header is required for POST, PATCH and DELETE requests",
        )
    print(f"Found valid CSRF token: {token}")
