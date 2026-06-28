from sqlalchemy.orm import Session
from app.models.user import User
from app.models.waitlist import Waitlist


# -----------------------------
# CORE ACTIVATION ENGINE
# -----------------------------
def activate_user_from_waitlist(db: Session, waitlist_entry: Waitlist):

    user = db.query(User).filter(User.id == waitlist_entry.user_id).first()

    if not user:
        return None

    user.status = "ACTIVE"
    user.department_id = waitlist_entry.department_id
    user.role = "member"

    return user