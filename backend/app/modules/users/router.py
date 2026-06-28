from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.core.deps import get_current_user
from app.core.responses import success_response
from app.models.department import Department

from app.modules.users.schemas import (
    UserCreate,
    UserOut,
    CompleteProfileRequest,
)

from app.modules.users.service import (
    create_user,
    get_users,
    complete_profile,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# =========================
# CREATE USER
# =========================
@router.post("/", response_model=UserOut)
def add_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    return create_user(db, user)


# =========================
# GET ALL USERS
# =========================
@router.get("/")
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    users = get_users(db)

    return success_response(
        data=[
            {
                "id": u.id,
                "full_name": u.full_name,
                "email": u.email,
                "status": u.status,
                "profile_completed": u.profile_completed,
                "auth_provider": u.auth_provider,
                "provider_id": u.provider_id,
                "matric_number": u.matric_number,
                "level": u.level,
                "faculty": u.faculty,
                "department_id": u.department_id,
            }
            for u in users
        ],
        message="users fetched successfully",
    )


# =========================
# GET CURRENT USER
# =========================
@router.get("/me")
def me(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    department = None

    if user.department_id:
        department_obj = (
            db.query(Department)
            .filter(Department.id == user.department_id)
            .first()
        )

        if department_obj:
            department = department_obj.name

    return success_response(
        data={
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "status": user.status,
            "profile_completed": user.profile_completed,
            "matric_number": user.matric_number,
            "level": user.level,
            "faculty": user.faculty,
            "department": department,
            "department_id": user.department_id,
        },
        message="user profile",
    )


# =========================
# COMPLETE PROFILE
# =========================
@router.patch("/me/profile")
def update_profile(
    payload: CompleteProfileRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    user = complete_profile(
        db=db,
        user=current_user,
        full_name=payload.full_name,
        matric_number=payload.matric_number,
        level=payload.level,
        faculty=payload.faculty,
        department_name=payload.department,
    )

    return success_response(
        data={
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "matric_number": user.matric_number,
            "level": user.level,
            "faculty": user.faculty,
            "department_id": user.department_id,
            "status": user.status,
            "profile_completed": user.profile_completed,
        },
        message="profile updated",
    )