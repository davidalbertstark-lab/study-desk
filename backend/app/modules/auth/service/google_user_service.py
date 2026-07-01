from sqlalchemy.orm import Session

from app.models.user import User


def get_or_create_google_user(
    db: Session,
    payload: dict
) -> User:
    """
    Takes verified Google ID token payload and:
    - finds existing user OR
    - creates a new user
    """

    google_sub = payload.get("sub")
    email = payload.get("email")
    full_name = payload.get("name")

    if not google_sub or not email:
        raise ValueError("Invalid Google payload")

    # =========================
    # 1. Check if user exists
    # =========================
    user = db.query(User).filter(
        User.provider_id == google_sub
    ).first()

    if user:
        return user

    # =========================
    # 2. Fallback: check email (important edge case)
    # =========================
    user_by_email = db.query(User).filter(
        User.email == email
    ).first()

    if user_by_email:
        # Link Google account to existing account
        user_by_email.auth_provider = "google"
        user_by_email.provider_id = google_sub

        db.commit()
        db.refresh(user_by_email)

        return user_by_email

    # =========================
    # 3. Create new user
    # =========================
    new_user = User(
        email=email,
        full_name=full_name,
        auth_provider="google",
        provider_id=google_sub,
        status="WAITLISTED",  # or ACTIVE depending on your flow
        profile_completed=False,
        hashed_password=None,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user