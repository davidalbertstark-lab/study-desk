from fastapi import APIRouter, Depends, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.responses import success_response
from app.core.deps import get_current_user
from app.core.config import settings

from app.modules.auth.schemas import (
    UserCreate,
    UserLogin,
    RefreshTokenRequest,
    ForgotPasswordRequest,
    VerifyResetCodeRequest,
    ResetPasswordRequest,
    VerifyRegistrationRequest,
    CompleteRegistrationRequest,
    ResendRegistrationCodeRequest,
    GoogleTicketRequest,
)

from app.models.user import User

from app.modules.auth.facade.auth_facade import AuthFacade

from urllib.parse import quote


router = APIRouter(prefix="/auth", tags=["Auth"])


# =========================
# FACADE DEPENDENCY
# =========================
def get_auth_facade(db: Session = Depends(get_db)) -> AuthFacade:
    return AuthFacade(db)


# =========================
# REGISTER FLOW
# =========================

@router.post("/register", operation_id="auth_register_user")
def register(payload: UserCreate, auth: AuthFacade = Depends(get_auth_facade)):

    auth.start_registration(payload.email, payload.password)

    return success_response(
        data={"email": payload.email},
        message="Verification code sent",
    )


@router.post("/verify-registration", operation_id="auth_verify_registration")
def verify_registration(
    payload: VerifyRegistrationRequest,
    auth: AuthFacade = Depends(get_auth_facade),
):

    auth.verify_registration(payload.email, payload.code)

    return success_response(
        data={"verified": True},
        message="Email verified",
    )


@router.post("/complete-registration", operation_id="auth_complete_registration")
def complete_registration(
    payload: CompleteRegistrationRequest,
    auth: AuthFacade = Depends(get_auth_facade),
):

    result = auth.complete_registration(payload.email)

    return success_response(
        data=result,
        message="Registration completed",
    )


@router.post("/resend-registration-code", operation_id="auth_resend_registration_code")
def resend_registration(
    payload: ResendRegistrationCodeRequest,
    auth: AuthFacade = Depends(get_auth_facade),
):

    auth.resend_registration(payload.email)

    return success_response(
        data={"resent": True},
        message="Verification code sent",
    )


# =========================
# GOOGLE OAUTH
# =========================

@router.get("/google/login", operation_id="auth_google_login")
def google_login(auth: AuthFacade = Depends(get_auth_facade)):

    return RedirectResponse(
        auth.get_google_login_url(),
        status_code=302,
    )


@router.get("/google/callback", operation_id="auth_google_callback")
def google_callback(
    code: str = Query(...),
    auth: AuthFacade = Depends(get_auth_facade),
):

    result = auth.handle_google_callback(code)

    ticket = result["ticket"]

    return RedirectResponse(
    url=f"{settings.FRONTEND_URL}/auth/google/callback?ticket={quote(ticket)}",
        status_code=302,
    )


# =========================
# LOGIN
# =========================

@router.post("/login", operation_id="auth_login_user")
def login(
    payload: UserLogin,
    auth: AuthFacade = Depends(get_auth_facade),
):

    result = auth.login(
        email=payload.email,
        password=payload.password,
        device_id=payload.device_id,
        remember_me=payload.remember_me,
    )

    return success_response(
        data=result,
        message="Login successful",
    )


# =========================
# TOKEN REFRESH
# =========================

@router.post("/refresh", operation_id="auth_refresh_token")
def refresh(
    payload: RefreshTokenRequest,
    auth: AuthFacade = Depends(get_auth_facade),
):

    result = auth.refresh_token(payload.refresh_token)

    return success_response(
        data=result,
        message="Token refreshed",
    )


# =========================
# LOGOUT
# =========================

@router.post("/logout", operation_id="auth_logout")
def logout(
    payload: RefreshTokenRequest,
    auth: AuthFacade = Depends(get_auth_facade),
):

    auth.logout(payload.refresh_token)

    return success_response(
        data={"logged_out": True},
        message="Session terminated",
    )


# =========================
# LOGOUT ALL
# =========================

@router.post("/logout-all", operation_id="auth_logout_all")
def logout_all(
    user: User = Depends(get_current_user),
    auth: AuthFacade = Depends(get_auth_facade),
):

    auth.logout_all(user.id)

    return success_response(
        data={"logged_out_all": True},
        message="All sessions revoked",
    )


# =========================
# PASSWORD RESET FLOW
# =========================

@router.post("/forgot-password")
def forgot_password(
    payload: ForgotPasswordRequest,
    auth: AuthFacade = Depends(get_auth_facade),
):

    auth.forgot_password(payload.email)

    return success_response(
        data={"sent": True},
        message="If email exists, reset code was sent",
    )


@router.post("/verify-reset-code")
def verify_reset(
    payload: VerifyResetCodeRequest,
    auth: AuthFacade = Depends(get_auth_facade),
):

    auth.verify_reset_code(payload.email, payload.code)

    return success_response(
        data={"verified": True},
        message="Code verified",
    )


@router.post("/reset-password")
def reset_password(
    payload: ResetPasswordRequest,
    auth: AuthFacade = Depends(get_auth_facade),
):

    auth.reset_password(
        payload.email,
        payload.code,
        payload.new_password,
    )

    return success_response(
        data={"reset": True},
        message="Password updated successfully",
    )


@router.post("/google/exchange-ticket")
def exchange_google_ticket(
    payload: GoogleTicketRequest,
):
    from app.modules.auth.service.login_ticket_service import (
        exchange_login_ticket,
    )

    result = exchange_login_ticket(payload.ticket)

    return success_response(
        data=result,
        message="Google login successful",
    )