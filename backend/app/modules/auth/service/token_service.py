from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token
)

from app.core.device import get_or_create_device_id


def create_auth_tokens(
    user,
    device_id: str | None = None,
    remember_me: bool = False
):
    """
    Single source of truth for authentication token creation.
    """

    device_id = get_or_create_device_id(device_id)

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    refresh_token = create_refresh_token(
        data={"sub": str(user.id)},
        remember_me=remember_me
    )

    decoded = decode_refresh_token(refresh_token)

    if not decoded:
        raise Exception("Failed to generate refresh token")

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "decoded_refresh": decoded,
        "device_id": device_id
    }


def rotate_auth_tokens(
    user,
    device_id: str,
    remember_me: bool = False
):
    """
    Rotates access + refresh tokens while preserving device binding.
    """

    return create_auth_tokens(
        user=user,
        device_id=device_id,
        remember_me=remember_me
    )