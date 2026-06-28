from sqlalchemy.orm import Session
from app.models.department_leader import DepartmentLeader
from app.models.waitlist import Waitlist
from app.models.user import User
from app.modules.activation.service import activate_user_from_waitlist


# -----------------------------
# CORE: GET LEADER DEPARTMENTS
# -----------------------------
def get_leader_department_ids(db: Session, leader_id: int):
    return [
        d.department_id
        for d in db.query(DepartmentLeader)
        .filter(DepartmentLeader.user_id == leader_id)
        .all()
    ]


# -----------------------------
# CORE: CHECK LEADER
# -----------------------------
def is_leader(db: Session, user_id: int) -> bool:
    return db.query(DepartmentLeader).filter(
        DepartmentLeader.user_id == user_id
    ).first() is not None


# -----------------------------
# GET WAITLIST
# -----------------------------
def get_leader_department_waitlist(db: Session, leader_id: int):

    department_ids = get_leader_department_ids(db, leader_id)

    if not department_ids:
        return []

    return db.query(Waitlist).filter(
        Waitlist.department_id.in_(department_ids),
        Waitlist.status == "PENDING"
    ).all()


# -----------------------------
# APPROVAL CORE
# -----------------------------
    def leader_approve(db: Session, leader_id: int, waitlist_id: int):

    entry = db.query(Waitlist).filter(
        Waitlist.id == waitlist_id
    ).first()

    if not entry:
        return None

    if entry.department_id not in get_leader_department_ids(db, leader_id):
        return "UNAUTHORIZED"

    if entry.status != "PENDING":
        return entry

    # 1. update waitlist
    entry.status = "APPROVED"

    # 2. activate user
    user = activate_user_from_waitlist(db, entry)

    db.commit()
    db.refresh(entry)

    # ✅ HERE IS THE FIX YOU ASKED ABOUT
    return {
        "waitlist": entry,
        "user": user
    }


# -----------------------------
# REJECT CORE
# -----------------------------
def leader_reject(db: Session, leader_id: int, waitlist_id: int):

    entry = db.query(Waitlist).filter(
        Waitlist.id == waitlist_id
    ).first()

    if not entry:
        return None

    if entry.department_id not in get_leader_department_ids(db, leader_id):
        return "UNAUTHORIZED"

    if entry.status != "PENDING":
        return entry

    entry.status = "REJECTED"

    user = db.query(User).filter(User.id == entry.user_id).first()
    if user:
        user.status = "REJECTED"
        user.department_id = None
        user.role = "member"

    db.commit()
    db.refresh(entry)

    return entry



