from datetime import datetime, timedelta, timezone
import hashlib
import uuid   # ✅ FIXED MISSING IMPORT

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings

from fastapi.security import HTTPBearer

bearer_scheme = HTTPBearer()


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def normalize_password(password: str) -> str:
    if len(password.encode("utf-8")) > 72:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()
    return password


def hash_password(password: str) -> str:
    return pwd_context.hash(normalize_password(password))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(
        normalize_password(plain_password),
        hashed_password
    )


def _create_token(data: dict, expires_delta: timedelta, token_type: str) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + expires_delta

    to_encode.update({
        "exp": expire,
        "type": token_type
    })

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def create_access_token(data: dict) -> str:
    jti = str(uuid.uuid4())

    to_encode = data.copy()
    to_encode.update({
        "jti": jti,
        "type": "access"
    })

    return _create_token(
        to_encode,
        timedelta(minutes=30),
        "access"
    )


def create_refresh_token(data: dict, remember_me: bool = False) -> str:
    jti = str(uuid.uuid4())  # ✅ FIXED

    days = (
        settings.REFRESH_TOKEN_REMEMBER_DAYS
        if remember_me
        else settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    expire = datetime.now(timezone.utc) + timedelta(days=days)

    data.update({
        "exp": expire,
        "type": "refresh",
        "jti": jti
    })

    return jwt.encode(
        data,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
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
            algorithms=[settings.ALGORITHM]
        )

        if payload.get("type") != "refresh":
            return None

        return payload

    except JWTError:
        return None