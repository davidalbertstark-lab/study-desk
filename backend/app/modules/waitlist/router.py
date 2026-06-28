from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.deps import get_current_user
from app.core.responses import success_response

from app.models.user import User
from app.modules.waitlist.service import (
    join_waitlist,
    get_my_waitlist,
)

router = APIRouter(
    prefix="/waitlist",
    tags=["Waitlist"]
)


@router.post("/join")
def join(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    entry = join_waitlist(
        db=db,
        user=current_user
    )

    return success_response(
        data={
            "id": entry.id,
            "status": entry.status
        },
        message="added to waitlist"
    )


@router.get("/me")
def my_waitlist(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    data = get_my_waitlist(
        db=db,
        user=current_user
    )

    return success_response(
        data=data,
        message="waitlist fetched"
    )