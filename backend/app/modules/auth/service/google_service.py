from urllib.parse import urlencode

import httpx
from google.oauth2 import id_token
from google.auth.transport import requests

from app.core.config import settings


# ==========================================================
# GOOGLE OPENID CONFIG
# ==========================================================

def get_google_provider_config() -> dict:
    """
    Fetch Google's OpenID configuration.

    Contains:
        - authorization_endpoint
        - token_endpoint
        - jwks_uri
    """

    try:
        response = httpx.get(
            settings.GOOGLE_DISCOVERY_URL,
            timeout=10.0
        )

        response.raise_for_status()

        return response.json()

    except httpx.RequestError as e:
        raise RuntimeError(
            f"Failed to fetch Google discovery document: {str(e)}"
        )


# ==========================================================
# AUTH URL BUILDER
# ==========================================================

def build_google_login_url() -> str:
    """
    Build Google OAuth login URL.

    This is used to redirect users to Google consent screen.
    """

    config = get_google_provider_config()

    authorization_endpoint = config["authorization_endpoint"]

    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "prompt": "select_account",
        "access_type": "offline",
    }

    return authorization_endpoint + "?" + urlencode(params)


# ==========================================================
# TOKEN EXCHANGE
# ==========================================================

def exchange_code_for_tokens(code: str) -> dict:
    """
    Exchange authorization code for Google tokens.

    Returns:
        {
            access_token,
            id_token,
            refresh_token (optional),
            expires_in,
            token_type
        }
    """

    config = get_google_provider_config()

    token_endpoint = config["token_endpoint"]

    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    try:
        response = httpx.post(
            token_endpoint,
            data=data,
            timeout=10.0
        )

        response.raise_for_status()

        return response.json()

    except httpx.RequestError as e:
        raise RuntimeError(
            f"Google token exchange failed: {str(e)}"
        )


# ==========================================================
# ID TOKEN VERIFICATION
# ==========================================================

def verify_google_id_token(token: str) -> dict:
    """
    Verifies Google ID token signature and claims.

    Ensures:
        - token is valid
        - issued by Google
        - audience matches your client_id
    """

    if not settings.GOOGLE_CLIENT_ID:
        raise ValueError("GOOGLE_CLIENT_ID is not configured")

    try:
        payload = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            settings.GOOGLE_CLIENT_ID,
        )

        return payload

    except Exception as e:
        raise ValueError(
            f"Google ID token verification failed: {str(e)}"
        )