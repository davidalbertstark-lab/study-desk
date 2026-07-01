from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
)

from app.db.base import Base


class PendingRegistration(Base):
    __tablename__ = "pending_registrations"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # =========================
    # Identity
    # =========================
    email = Column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )

    password_hash = Column(
        String,
        nullable=False,
    )

    # =========================
    # Email Verification
    # =========================
    verification_code_hash = Column(
        String,
        nullable=False,
    )

    verification_code_expires_at = Column(
        DateTime,
        nullable=False,
    )

    verification_sent_at = Column(
        DateTime,
        nullable=False,
    )

    verification_attempts = Column(
        Integer,
        default=0,
        nullable=False,
    )

    is_verified = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    # =========================
    # Metadata
    # =========================
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )