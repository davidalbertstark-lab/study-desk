from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Index
from datetime import datetime, timezone
import uuid

from app.db.base import Base


class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)

    # user link
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # token identity
    refresh_token_jti = Column(String, unique=True, nullable=False, index=True)

    # 🧠 DEVICE TRACKING (NEW CORE FEATURE)
    device_id = Column(String, nullable=False, index=True)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)

    # session state
    is_active = Column(Boolean, default=True, nullable=False)

    # expiry
    expires_at = Column(DateTime, nullable=False)

    # lifecycle
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    revoked_at = Column(DateTime, nullable=True)


# indexes
Index("ix_user_sessions_user_active", UserSession.user_id, UserSession.is_active)
Index("ix_user_sessions_device", UserSession.device_id)
Index("ix_user_sessions_expiry", UserSession.expires_at)