from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.responses import success_response
from app.core.deps import get_current_user

from app.models.user import User

from app.modules.leaders.service import (
    get_leader_department_waitlist,
    leader_approve,
    leader_reject,
    is_leader
)

router = APIRouter(prefix="/leader", tags=["Leader"])


# -----------------------------
# VIEW WAITLIST
# -----------------------------
@router.get("/waitlist")
def leader_waitlist(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if not is_leader(db, current_user.id):
        raise HTTPException(status_code=403, detail="Not a leader")

    data = get_leader_department_waitlist(db, current_user.id)

    return success_response(
        data={
            "count": len(data),
            "waitlist": [
                {
                    "id": w.id,
                    "user_id": w.user_id,
                    "department_id": w.department_id,
                    "status": w.status,
                    "created_at": w.created_at
                }
                for w in data
            ]
        },
        message="leader waitlist fetched successfully"
    )


# -----------------------------
# APPROVE USER
# -----------------------------
@router.post("/approve/{waitlist_id}")
def approve(
    waitlist_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if not is_leader(db, current_user.id):
        raise HTTPException(status_code=403, detail="Not a leader")

    result = leader_approve(db, current_user.id, waitlist_id)

    if result == "UNAUTHORIZED":
        raise HTTPException(status_code=403, detail="Not allowed")

    if result is None:
        raise HTTPException(status_code=404, detail="Waitlist not found")

    return success_response(
        data={
            "waitlist": {
                "id": result["waitlist"].id,
                "status": result["waitlist"].status,
                "department_id": result["waitlist"].department_id
            },
            "user": {
                "id": result["user"].id,
                "status": result["user"].status,
                "department_id": result["user"].department_id,
                "role": result["user"].role
            }
        },
        message="user approved successfully"
    )


# -----------------------------
# REJECT USER
# -----------------------------
@router.post("/reject/{waitlist_id}")
def reject(
    waitlist_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if not is_leader(db, current_user.id):
        raise HTTPException(status_code=403, detail="Not a leader")

    result = leader_reject(db, current_user.id, waitlist_id)

    if result == "UNAUTHORIZED":
        raise HTTPException(status_code=403, detail="Not allowed")

    if result is None:
        raise HTTPException(status_code=404, detail="Waitlist not found")

    return success_response(
        data={
            "waitlist": {
                "id": result.id,
                "status": result.status,
                "department_id": result.department_id
            }
        },
        message="user rejected successfully"
    )