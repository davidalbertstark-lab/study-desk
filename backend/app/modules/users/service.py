from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.user import User
from app.models.department import Department
from app.modules.users.schemas import UserCreate


def create_user(db: Session, payload: UserCreate):

    user = User(
        email=payload.email
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def complete_profile(
    db: Session,
    user: User,
    full_name: str,
    matric_number: str,
    level: str,
    faculty: str,
    department_name: str,
):

    existing = (
        db.query(User)
        .filter(
            User.matric_number == matric_number,
            User.id != user.id
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Matric number already exists"
        )

    department = (
        db.query(Department)
        .filter(
            Department.name.ilike(department_name.strip())
        )
        .first()
    )

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    user.full_name = full_name
    user.matric_number = matric_number
    user.level = level
    user.faculty = faculty
    user.department_id = department.id

    user.profile_completed = True

    # profile completion does NOT approve user
    user.status = "WAITLISTED"

    db.commit()
    db.refresh(user)

    return user


def get_users(db: Session):

    return db.query(User).all()