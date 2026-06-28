from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime, timezone

from app.db.base import Base


class Waitlist(Base):
    __tablename__ = "waitlist"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), index=True, nullable=False)

    status = Column(String, default="PENDING", index=True)
    # PENDING | APPROVED | REJECTED

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # 🔥 ADD THIS (IMPORTANT FOR AUDIT TRAIL)
    processed_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    processed_at = Column(DateTime, nullable=True)