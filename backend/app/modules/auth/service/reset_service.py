from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.user import User
from app.core.rate_limit import is_rate_limited
from app.core.email import send_reset_code_email
from app.core.security import (
    generate_reset_code,
    hash_reset_code,
    verify_reset_code,
    hash_password
)


# =========================
# 1. FORGOT PASSWORD
# =========================
def create_password_reset_code(db: Session, email: str):

    if is_rate_limited(email):
        raise HTTPException(
            status_code=429,
            detail="Too many requests"
        )

    user = db.query(User).filter(User.email == email).first()

    # prevent user enumeration
    if not user:
        return True

    code = generate_reset_code()

    user.reset_code_hash = hash_reset_code(code)
    user.reset_code_expires_at = datetime.now() + timedelta(minutes=10)
    user.reset_attempts = 0
    user.reset_verified = False

    db.commit()

    print(f"[RESET] Generated code for {user.email}: {code}")

    sent = send_reset_code_email(user.email, code)

    print(f"[RESET] Email sent: {sent}")

    # TODO: email service integration
    # email_service.send_reset_code(user.email, code)

    return True


# =========================
# 2. VERIFY RESET CODE
# =========================
def verify_reset_code_service(db: Session, email: str, code: str):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        return False

    if not user.reset_code_hash or not user.reset_code_expires_at:
        return False

    # expiry check
    if user.reset_code_expires_at < datetime.now():
        return False

    # attempt tracking (security hardening)
    user.reset_attempts += 1

    if user.reset_attempts > 5:
        raise HTTPException(
            status_code=429,
            detail="Too many invalid attempts"
        )

    valid = verify_reset_code(code, user.reset_code_hash)

    if valid:
        user.reset_verified = True

    db.commit()

    return valid


# =========================
# 3. RESET PASSWORD
# =========================
def reset_user_password(
    db: Session,
    email: str,
    code: str,
    new_password: str
):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 🔥 CRITICAL SECURITY GATE
    if not user.reset_verified:
        raise HTTPException(
            status_code=403,
            detail="Reset not verified"
        )

    # optional: re-check code validity (extra safety layer)
    if not verify_reset_code_service(db, email, code):
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired code"
        )

    if new_password.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Password cannot be empty"
        )

    user.hashed_password = hash_password(new_password)

    # =========================
    # CLEAN RESET STATE
    # =========================
    user.reset_code_hash = None
    user.reset_code_expires_at = None
    user.reset_attempts = 0
    user.reset_verified = False

    # =========================
    # SECURITY-FIRST DECISION (A)
    # revoke sessions here (IMPORTANT)
    # =========================
    from app.modules.auth.service.session_service import logout_all_sessions

    logout_all_sessions(db, user.id)

    db.commit()

    return True