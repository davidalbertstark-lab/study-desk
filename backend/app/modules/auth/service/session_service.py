from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models.session import UserSession
from app.core.device import get_or_create_device_id
from app.core.security import decode_refresh_token


# =========================
# CREATE SESSION
# =========================
def create_session(
    db: Session,
    user_id: int,
    decoded_refresh: dict,
    device_id: str | None
):
    """
    Creates a new login session from a decoded refresh token.
    """

    device_id = get_or_create_device_id(device_id)

    session = UserSession(
        user_id=user_id,
        refresh_token_jti=decoded_refresh["jti"],
        device_id=device_id,
        ip_address=None,
        user_agent=None,
        is_active=True,
        expires_at=datetime.fromtimestamp(
            decoded_refresh["exp"],
            tz=timezone.utc
        )
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


# =========================
# DEACTIVATE DEVICE SESSIONS
# =========================
def deactivate_device_sessions(
    db: Session,
    user_id: int,
    device_id: str
):
    """
    Deactivates all sessions for a specific device.
    """

    db.query(UserSession).filter(
        UserSession.user_id == user_id,
        UserSession.device_id == device_id,
        UserSession.is_active == True
    ).update({"is_active": False})

    db.commit()


# =========================
# REVOKE SESSION BY JTI
# =========================
def revoke_session(db: Session, jti: str):

    session = db.query(UserSession).filter(
        UserSession.refresh_token_jti == jti,
        UserSession.is_active == True
    ).first()

    if session:
        session.is_active = False
        session.revoked_at = datetime.now(timezone.utc)
        db.commit()

    return True


# =========================
# GET ACTIVE SESSION
# =========================
def get_active_session(db: Session, jti: str):

    return db.query(UserSession).filter(
        UserSession.refresh_token_jti == jti,
        UserSession.is_active == True
    ).first()


# =========================
# LOGOUT ALL SESSIONS
# =========================
def logout_all_sessions(db: Session, user_id: int):

    sessions = db.query(UserSession).filter(
        UserSession.user_id == user_id,
        UserSession.is_active == True
    ).all()

    now = datetime.now(timezone.utc)

    for session in sessions:
        session.is_active = False
        session.revoked_at = now

    db.commit()

    return True


# =========================
# ROTATE SESSION
# =========================
def rotate_session(
    db: Session,
    old_jti: str,
    user_id: int,
    decoded_refresh: dict,
    device_id: str
):
    """
    Secure refresh-token rotation.

    Old session becomes unusable.
    New refresh session is created.
    """

    revoke_session(db, old_jti)

    return create_session(
        db=db,
        user_id=user_id,
        decoded_refresh=decoded_refresh,
        device_id=device_id
    )