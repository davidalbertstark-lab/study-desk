from fastapi import Depends, HTTPException

from app.core.deps import get_current_user
from app.models.user import User


def require_completed_profile(
    user: User = Depends(get_current_user)
):

    if not user.profile_completed:
        raise HTTPException(
            status_code=403,
            detail="Profile not completed"
        )

    return user


def require_active_user(
    user: User = Depends(require_completed_profile)
):

    if user.status != "ACTIVE":
        raise HTTPException(
            status_code=403,
            detail="Account awaiting approval"
        )

    return user