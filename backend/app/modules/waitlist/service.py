from sqlalchemy.orm import Session
from app.models.waitlist import Waitlist
from app.modules.waitlist.schemas import WaitlistJoin

from datetime import datetime, timezone
from app.models.user import User
from app.models.department import Department

def join_waitlist(
    db: Session,
    user: User
):

    existing = (
        db.query(Waitlist)
        .filter(Waitlist.user_id == user.id)
        .first()
    )

    if existing:
        return existing

    entry = Waitlist(
        user_id=user.id,
        department_id=user.department_id,
        status="PENDING"
    )

    db.add(entry)
    db.commit()
    db.refresh(entry)

    return entry


def approve_waitlist(db: Session, waitlist_id: int):
    entry = db.query(Waitlist).filter(
        Waitlist.id == waitlist_id
    ).first()

    if not entry:
        return None

    # -------------------------
    # 1. Update waitlist
    # -------------------------
    entry.status = "APPROVED"
    entry.processed_at = datetime.now(timezone.utc)

    # -------------------------
    # 2. Update user (CRITICAL)
    # -------------------------
    user = db.query(User).filter(
        User.id == entry.user_id
    ).first()

    if user:
        user.status = "ACTIVE"
        user.department_id = entry.department_id
        user.role = "member"

    db.commit()

    db.refresh(entry)

    return entry


# -----------------------------
# REJECT WAITLIST ENTRY (SOURCE OF TRUTH)
# -----------------------------
def reject_waitlist(db: Session, waitlist_id: int):

    entry = db.query(Waitlist).filter(
        Waitlist.id == waitlist_id
    ).first()

    if not entry:
        return None

    entry.status = "REJECTED"
    entry.processed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(entry)

    return entry


def get_my_waitlist(db: Session, user: User):

    entry = (
        db.query(Waitlist)
        .filter(Waitlist.user_id == user.id)
        .first()
    )

    if not entry:
        return None

    department = (
        db.query(Department)
        .filter(Department.id == entry.department_id)
        .first()
    )

    return {
        "full_name": user.full_name,
        "matric_number": user.matric_number,
        "department": department.name if department else None,
        "status": entry.status
    }