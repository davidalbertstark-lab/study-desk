from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.pending_registration import PendingRegistration

from app.core.rate_limit import is_rate_limited

from app.core.email import (
    send_registration_code_email,
)

from app.core.security import (
    generate_verification_code,
    hash_verification_code,
    verify_verification_code,
    hash_password,
)


# =========================
# START REGISTRATION
# =========================
def start_registration(
    db: Session,
    email: str,
    password: str,
):
    """
    Starts the registration flow.

    Instead of creating a real User immediately,
    we create/update a PendingRegistration and
    send a verification code.
    """

    if password.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Password cannot be empty",
        )

    if is_rate_limited(email):
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please try again later.",
        )

    # -------------------------
    # Existing real account?
    # -------------------------
    existing_user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    code = generate_verification_code()

    password_hash = hash_password(password)

    code_hash = hash_verification_code(code)

    now = datetime.utcnow()

    expires_at = now + timedelta(minutes=10)

    pending = (
        db.query(PendingRegistration)
        .filter(PendingRegistration.email == email)
        .first()
    )

    if pending:

        pending.password_hash = password_hash
        pending.verification_code_hash = code_hash
        pending.verification_code_expires_at = expires_at
        pending.verification_sent_at = now
        pending.verification_attempts = 0
        pending.is_verified = False

    else:

        pending = PendingRegistration(
            email=email,
            password_hash=password_hash,
            verification_code_hash=code_hash,
            verification_code_expires_at=expires_at,
            verification_sent_at=now,
            verification_attempts=0,
            is_verified=False,
        )

        db.add(pending)

    db.commit()

    sent = send_registration_code_email(
        to_email=email,
        code=code,
    )

    if not sent:
        raise HTTPException(
            status_code=500,
            detail="Failed to send verification email",
        )

    return True


# =========================
# VERIFY REGISTRATION CODE
# =========================
def verify_registration_code(
    db: Session,
    email: str,
    code: str,
):
    """
    Verifies the registration OTP.

    Does NOT create the real user yet.
    """

    pending = (
        db.query(PendingRegistration)
        .filter(PendingRegistration.email == email)
        .first()
    )

    if not pending:
        raise HTTPException(
            status_code=404,
            detail="Registration not found",
        )

    if pending.verification_code_expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=400,
            detail="Verification code has expired",
        )

    pending.verification_attempts += 1

    if pending.verification_attempts > 5:
        raise HTTPException(
            status_code=429,
            detail="Too many invalid attempts",
        )

    valid = verify_verification_code(
        code,
        pending.verification_code_hash,
    )

    if not valid:
        db.commit()

        raise HTTPException(
            status_code=400,
            detail="Invalid verification code",
        )

    pending.is_verified = True

    db.commit()

    return True



# =========================
# COMPLETE REGISTRATION
# =========================
def complete_registration(
    db: Session,
    email: str,
):
    """
    Creates the real User after successful
    email verification.

    Deletes the PendingRegistration afterwards.
    """

    pending = (
        db.query(PendingRegistration)
        .filter(PendingRegistration.email == email)
        .first()
    )

    if not pending:
        raise HTTPException(
            status_code=404,
            detail="Registration not found",
        )

    if not pending.is_verified:
        raise HTTPException(
            status_code=403,
            detail="Email has not been verified",
        )

    existing_user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    user = User(
        email=pending.email,
        hashed_password=pending.password_hash,
        status="WAITLISTED",
        profile_completed=False,
    )

    db.add(user)

    db.flush()

    db.delete(pending)

    db.commit()

    db.refresh(user)

    return user


# =========================
# RESEND REGISTRATION CODE
# =========================
def resend_registration_code(
    db: Session,
    email: str,
):
    """
    Generates a new verification code
    for an existing pending registration.
    """

    if is_rate_limited(email):
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please try again later.",
        )

    pending = (
        db.query(PendingRegistration)
        .filter(PendingRegistration.email == email)
        .first()
    )

    if not pending:
        raise HTTPException(
            status_code=404,
            detail="Registration not found",
        )

    if pending.is_verified:
        raise HTTPException(
            status_code=400,
            detail="Registration already verified",
        )

    code = generate_verification_code()

    now = datetime.utcnow()

    pending.verification_code_hash = hash_verification_code(code)
    pending.verification_code_expires_at = now + timedelta(minutes=10)
    pending.verification_sent_at = now
    pending.verification_attempts = 0

    db.commit()

    sent = send_registration_code_email(
        to_email=email,
        code=code,
    )

    if not sent:
        raise HTTPException(
            status_code=500,
            detail="Failed to send verification email",
        )

    return True


# =========================
# DELETE EXPIRED REGISTRATION
# =========================
def delete_expired_pending_registration(
    db: Session,
    email: str,
):
    """
    Deletes one expired pending registration.
    """

    pending = (
        db.query(PendingRegistration)
        .filter(PendingRegistration.email == email)
        .first()
    )

    if not pending:
        return False

    if pending.verification_code_expires_at > datetime.utcnow():
        return False

    db.delete(pending)
    db.commit()

    return True


# =========================
# CLEANUP EXPIRED REGISTRATIONS
# =========================
def cleanup_expired_pending_registrations(
    db: Session,
):
    """
    Removes every expired pending registration.
    Intended for scheduled jobs.
    """

    expired = (
        db.query(PendingRegistration)
        .filter(
            PendingRegistration.verification_code_expires_at
            < datetime.utcnow()
        )
        .all()
    )

    for registration in expired:
        db.delete(registration)

    db.commit()

    return len(expired)