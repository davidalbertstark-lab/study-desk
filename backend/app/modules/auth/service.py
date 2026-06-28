from sqlalchemy.orm import Session
from app.models.user import User
from fastapi import HTTPException
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)

# -------------------
# REGISTER USER
# -------------------
def register_user(
    db: Session,
    email: str,
    password: str
):
    if password.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Password cannot be empty."
        )
    existing_user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    user = User(
        email=email,
        hashed_password=hash_password(password),
        status="WAITLISTED",
        profile_completed=False
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# -------------------
# AUTHENTICATE USER
# -------------------
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


# -------------------
# LOGIN TOKEN (OPTIONAL UTILITY)
# -------------------
def login_user(user: User):
    return create_access_token({
        "sub": str(user.id),
        "email": user.email,
        "role": "user"
    })