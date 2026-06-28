from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from datetime import datetime, timezone

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    # identity
    full_name = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    matric_number = Column(String, unique=True, nullable=True)
    level = Column(String, nullable=True)
    faculty = Column(String, nullable=True)

    # auth provider support
    auth_provider = Column(String, default="local")  # local | google
    provider_id = Column(String, nullable=True, index=True)

    # system state
    status = Column(String, default="WAITLISTED")
    # WAITLISTED | ACTIVE | REJECTED

    role = Column(String, default="member")
    # leader | sub_leader | manager | member

    department_id = Column(
        Integer,
        ForeignKey("departments.id", use_alter=True),
        nullable=True,
        index=True
    )

    profile_completed = Column(Boolean, default=False)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))