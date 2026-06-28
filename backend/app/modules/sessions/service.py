from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.models.session import UserSession


def cleanup_expired_sessions(db: Session):
    """
    Permanently remove expired sessions (DB hygiene)
    """
    now = datetime.now(timezone.utc)

    db.query(UserSession).filter(
        UserSession.expires_at < now
    ).delete()

    db.commit()


def cleanup_inactive_sessions(db: Session, user_id: int):
    """
    Remove old inactive sessions for a specific user
    (prevents session spam buildup)
    """

    db.query(UserSession).filter(
        UserSession.user_id == user_id,
        UserSession.is_active == False
    ).delete()

    db.commit()