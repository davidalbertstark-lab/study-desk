from sqlalchemy.orm import Session

from app.modules.auth.exceptions import InvalidCredentialsError, UserNotFoundError

from app.modules.auth.service.registration_service import (
    start_registration,
    verify_registration_code,
    complete_registration,
    resend_registration_code,
)

from app.modules.auth.service.auth_service import authenticate_user

from app.modules.auth.service.google_callback_service import handle_google_login

from app.modules.auth.service.token_service import create_auth_tokens

from app.modules.auth.service.session_service import (
    create_session,
    revoke_session,
    logout_all_sessions,
    get_active_session,
    rotate_session,
)

from app.modules.auth.service.reset_service import (
    create_password_reset_code,
    verify_reset_code_service,
    reset_user_password,
)

from app.models.user import User

from app.core.security import decode_refresh_token


class AuthFacade:
    """
    Single entry point for ALL authentication flows.

    This removes orchestration logic from router
    and centralizes auth lifecycle management.
    """

    def __init__(self, db: Session):
        self.db = db

    # =========================
    # REGISTRATION FLOW
    # =========================

    def start_registration(self, email: str, password: str):
        return start_registration(
            db=self.db,
            email=email,
            password=password,
        )

    def verify_registration(self, email: str, code: str):
        return verify_registration_code(
            db=self.db,
            email=email,
            code=code,
        )

    def complete_registration(self, email: str):
        user = complete_registration(
            db=self.db,
            email=email,
        )

        tokens = create_auth_tokens(
            user=user,
            remember_me=False,
        )

        create_session(
            db=self.db,
            user_id=user.id,
            decoded_refresh=tokens["decoded_refresh"],
            device_id=tokens["device_id"],
        )

        return {
            "user": {
                "id": user.id,
                "email": user.email,
                "status": user.status,
                "profile_completed": user.profile_completed,
            },
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
            "device_id": tokens["device_id"],
            "token_type": "bearer",
        }

    def resend_registration(self, email: str):
        return resend_registration_code(
            db=self.db,
            email=email,
        )

    # =========================
    # LOGIN FLOW
    # =========================

    def login(self, email: str, password: str, device_id=None, remember_me=False):

        user = authenticate_user(self.db, email, password)

        if not user:
            raise InvalidCredentialsError()

        tokens = create_auth_tokens(
            user=user,
            device_id=device_id,
            remember_me=remember_me,
        )

        create_session(
            db=self.db,
            user_id=user.id,
            decoded_refresh=tokens["decoded_refresh"],
            device_id=tokens["device_id"],
        )

        return {
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "status": user.status,
                "profile_completed": user.profile_completed,
            },
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
            "device_id": tokens["device_id"],
            "token_type": "bearer",
        }

    # =========================
    # GOOGLE FLOW
    # =========================

    def get_google_login_url(self):
        from app.modules.auth.service.google_service import build_google_login_url
        return build_google_login_url()

    def handle_google_callback(self, code: str):

        result = handle_google_login(
            db=self.db,
            code=code,
        )

        return result

    # =========================
    # REFRESH FLOW
    # =========================

    def refresh_token(self, refresh_token: str):

        decoded = decode_refresh_token(refresh_token)

        if not decoded:
            raise InvalidTokenError()

        session = get_active_session(self.db, decoded["jti"])

        if not session:
            raise SessionNotFoundError()

        user = self.db.query(User).filter(
            User.id == int(decoded["sub"])
        ).first()

        if not user:
            raise UserNotFoundError()

        tokens = create_auth_tokens(
            user=user,
            device_id=session.device_id,
            remember_me=False,
        )

        rotate_session(
            db=self.db,
            old_jti=decoded["jti"],
            user_id=user.id,
            decoded_refresh=tokens["decoded_refresh"],
            device_id=session.device_id,
        )

        return {
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
            "token_type": "bearer",
        }

    # =========================
    # LOGOUT FLOW
    # =========================

    def logout(self, refresh_token: str):

        decoded = decode_refresh_token(refresh_token)

        if decoded:
            revoke_session(self.db, decoded["jti"])

        return True

    def logout_all(self, user_id: int):

        return logout_all_sessions(self.db, user_id)

    # =========================
    # PASSWORD RESET FLOW
    # =========================

    def forgot_password(self, email: str):

        return create_password_reset_code(self.db, email)

    def verify_reset_code(self, email: str, code: str):

        return verify_reset_code_service(
            self.db,
            email,
            code,
        )

    def reset_password(self, email: str, code: str, new_password: str):

        return reset_user_password(
            self.db,
            email,
            code,
            new_password,
        )