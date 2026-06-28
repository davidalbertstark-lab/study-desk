from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.db.session import get_db
from app.modules.auth.service import register_user, authenticate_user
from app.modules.auth.schemas import (
    UserCreate,
    UserLogin,
    RefreshTokenRequest
)
from app.core.responses import success_response
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    decode_access_token   # 🔥 ADD THIS
)

from app.models.session import UserSession
from app.modules.sessions.service import cleanup_inactive_sessions
from app.core.deps import get_current_user
from app.models.user import User
from app.core.device import get_or_create_device_id

router = APIRouter(prefix="/auth", tags=["Auth"])


# =========================
# REGISTER
# =========================
@router.post("/register", operation_id="auth_register_user")
def register(payload: UserCreate, db: Session = Depends(get_db)):

    user = register_user(
        db,
        payload.email,
        payload.password
    )

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    refresh_token = create_refresh_token(
        data={"sub": str(user.id)}
    )

    decoded = decode_refresh_token(refresh_token)

    device_id = get_or_create_device_id(None)

    session = UserSession(
        user_id=user.id,
        refresh_token_jti=decoded["jti"],
        device_id=device_id,
        ip_address=None,
        user_agent=None,
        is_active=True,
        expires_at=datetime.fromtimestamp(
            decoded["exp"],
            tz=timezone.utc
        )
    )

    db.add(session)
    db.commit()

    return success_response(
        data={
            "user": {
                "id": user.id,
                "email": user.email,
                "status": user.status,
                "profile_completed": user.profile_completed,
            },
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        },
        message="user created"
    )


# =========================
# LOGIN
# =========================
@router.post("/login", operation_id="auth_login_user")
def login(payload: UserLogin, db: Session = Depends(get_db)):

    user = authenticate_user(db, payload.email, payload.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    cleanup_inactive_sessions(db, user.id)

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    refresh_token = create_refresh_token(
        data={"sub": str(user.id)},
        remember_me=payload.remember_me
    )

    decoded = decode_refresh_token(refresh_token)

    if not decoded:
        raise HTTPException(status_code=500, detail="Token generation failed")

    jti = decoded["jti"]

    # 🧠 DEVICE INFO EXTRACTION
    device_id = get_or_create_device_id(
        payload.device_id
    )

    ip_address = None
    user_agent = None

    # safe request access
    # (FastAPI injects request if needed later)

    # 🧠 DEACTIVATE OLD SESSIONS (same device only optional strategy)
    db.query(UserSession).filter(
        UserSession.user_id == user.id,
        UserSession.device_id == device_id,
        UserSession.is_active == True
    ).update({"is_active": False})

    # 🧠 CREATE NEW DEVICE SESSION
    session = UserSession(
        user_id=user.id,
        refresh_token_jti=jti,
        device_id=device_id,
        ip_address=ip_address,
        user_agent=user_agent,
        is_active=True,
        expires_at=datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return success_response(
        data={
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "status": user.status,
                "profile_completed": user.profile_completed   # ✅ ADD THIS
            },
            "access_token": access_token,
            "refresh_token": refresh_token,
            "device_id": device_id,
            "token_type": "bearer"
        },
        message="login successful"
    )


# =========================
# REFRESH TOKEN
# =========================
@router.post("/refresh", operation_id="auth_refresh_token")
def refresh(payload: RefreshTokenRequest, db: Session = Depends(get_db)):

    token = payload.refresh_token

    if not token:
        raise HTTPException(status_code=400, detail="Refresh token required")

    decoded = decode_refresh_token(token)

    if not decoded:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    user_id = decoded.get("sub")
    jti = decoded.get("jti")

    if not user_id or not jti:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    now = datetime.now(timezone.utc)

    session = db.query(UserSession).filter(
        UserSession.refresh_token_jti == jti,
        UserSession.is_active == True,
        UserSession.expires_at > now
    ).first()

    if not session:
        raise HTTPException(status_code=401, detail="Session expired or revoked")

    # rotate session
    session.is_active = False
    session.revoked_at = now

    new_access_token = create_access_token(
        data={"sub": user_id}
    )

    new_refresh_token = create_refresh_token(
        data={"sub": user_id}
    )

    new_decoded = decode_refresh_token(new_refresh_token)

    new_session = UserSession(
        user_id=int(user_id),
        refresh_token_jti=new_decoded["jti"],

        device_id=session.device_id,
        ip_address=session.ip_address,
        user_agent=session.user_agent,

        is_active=True,

        expires_at=datetime.fromtimestamp(
            new_decoded["exp"],
            tz=timezone.utc
        )
    )

    db.add(new_session)
    db.commit()

    return success_response(
        data={
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        },
        message="token refreshed"
    )


# =========================
# LOGOUT (single session)
# =========================
@router.post("/logout", operation_id="auth_logout")
def logout(payload: RefreshTokenRequest, db: Session = Depends(get_db)):

    token = payload.refresh_token

    if not token:
        raise HTTPException(status_code=400, detail="Refresh token required")

    decoded = decode_refresh_token(token)

    if not decoded:
        raise HTTPException(status_code=401, detail="Invalid token")

    jti = decoded.get("jti")

    session = db.query(UserSession).filter(
        UserSession.refresh_token_jti == jti,
        UserSession.is_active == True
    ).first()

    if session:
        session.is_active = False
        session.revoked_at = datetime.now(timezone.utc)
        db.commit()

    return success_response(
        data={"logged_out": True},
        message="session terminated"
    )


# =========================
# LOGOUT ALL SESSIONS
# =========================
@router.post("/logout-all", operation_id="auth_logout_all")
def logout_all(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    now = datetime.now(timezone.utc)

    sessions = db.query(UserSession).filter(
        UserSession.user_id == user.id,
        UserSession.is_active == True
    ).all()

    for session in sessions:
        session.is_active = False
        session.revoked_at = now

    db.commit()

    return success_response(
        data={"logged_out_all": True},
        message="all sessions revoked"
    )