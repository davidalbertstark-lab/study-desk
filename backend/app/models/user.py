from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from datetime import datetime, timezone

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    # =========================
    # Identity
    # =========================
    full_name = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)

    matric_number = Column(String, unique=True, nullable=True)
    level = Column(String, nullable=True)
    faculty = Column(String, nullable=True)

    # =========================
    # OAuth
    # =========================
    auth_provider = Column(String, default="local")  # local | google
    provider_id = Column(
        String,
        nullable=True,
        unique=True,
        index=True,
    )

    # =========================
    # Account State
    # =========================
    status = Column(String, default="WAITLISTED")
    # WAITLISTED | ACTIVE | REJECTED

    role = Column(String, default="member")
    # leader | sub_leader | manager | member

    department_id = Column(
        Integer,
        ForeignKey("departments.id", use_alter=True),
        nullable=True,
        index=True,
    )

    profile_completed = Column(Boolean, default=False)

    # =========================
    # Password Reset
    # =========================
    reset_code_hash = Column(String, nullable=True)

    reset_code_expires_at = Column(
        DateTime,
        nullable=True
    )

    reset_attempts = Column(
        Integer,
        default=0,
        nullable=False,
    )

    reset_verified = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    # =========================
    # Metadata
    # =========================
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )