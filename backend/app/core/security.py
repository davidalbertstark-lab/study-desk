from datetime import datetime, timedelta, timezone
import hashlib
import uuid
import secrets

from jose import jwt, JWTError
from passlib.context import CryptContext

from fastapi.security import HTTPBearer

from app.core.config import settings


bearer_scheme = HTTPBearer()


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# ==========================================================
# PASSWORD HELPERS
# ==========================================================

def normalize_password(password: str) -> str:
    """
    bcrypt only supports 72 bytes.

    Longer passwords are SHA256-normalized first so users
    can still use arbitrarily long passwords safely.
    """
    if len(password.encode("utf-8")) > 72:
        return hashlib.sha256(
            password.encode("utf-8")
        ).hexdigest()

    return password


def hash_password(password: str) -> str:
    return pwd_context.hash(
        normalize_password(password)
    )


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:

    return pwd_context.verify(
        normalize_password(plain_password),
        hashed_password,
    )


# ==========================================================
# JWT HELPERS
# ==========================================================

def _create_token(
    data: dict,
    expires_delta: timedelta,
    token_type: str,
) -> str:

    payload = data.copy()

    payload.update(
        {
            "exp": datetime.now(timezone.utc)
            + expires_delta,
            "type": token_type,
        }
    )

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def create_access_token(data: dict) -> str:

    payload = data.copy()

    payload.update(
        {
            "jti": str(uuid.uuid4()),
            "type": "access",
        }
    )

    return _create_token(
        payload,
        timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        ),
        "access",
    )


def create_refresh_token(
    data: dict,
    remember_me: bool = False,
) -> str:

    days = (
        settings.REFRESH_TOKEN_REMEMBER_DAYS
        if remember_me
        else settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    payload = data.copy()

    payload.update(
        {
            "exp": datetime.now(timezone.utc)
            + timedelta(days=days),
            "type": "refresh",
            "jti": str(uuid.uuid4()),
        }
    )

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def decode_access_token(token: str):

    try:

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        if payload.get("type") != "access":
            return None

        return payload

    except JWTError:
        return None


def decode_refresh_token(token: str):

    try:

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        if payload.get("type") != "refresh":
            return None

        return payload

    except JWTError:
        return None


# ==========================================================
# VERIFICATION CODE HELPERS
# ==========================================================

def generate_verification_code() -> str:
    """
    Generates a cryptographically secure 6-digit code.

    Used for:
        - Registration
        - Password reset
        - Email verification
        - Future 2FA
    """
    return f"{secrets.randbelow(1_000_000):06d}"


def hash_verification_code(code: str) -> str:
    """
    Stores only a SHA256 hash of verification codes.
    """
    return hashlib.sha256(
        code.encode()
    ).hexdigest()


def verify_verification_code(
    code: str,
    stored_hash: str | None,
) -> bool:

    if not stored_hash:
        return False

    return (
        hashlib.sha256(
            code.encode()
        ).hexdigest()
        == stored_hash
    )


# ==========================================================
# BACKWARD COMPATIBILITY
# ==========================================================
#
# Existing password-reset code currently imports these names.
# Keeping them avoids breaking the project while we migrate
# registration and reset flows to the generic helpers.
#

generate_reset_code = generate_verification_code
hash_reset_code = hash_verification_code
verify_reset_code = verify_verification_code