from sqlalchemy.orm import Session

from app.modules.auth.service.google_service import (
    exchange_code_for_tokens,
    verify_google_id_token
)

from app.modules.auth.service.google_user_service import (
    get_or_create_google_user
)

from app.modules.auth.service.token_service import create_auth_tokens
from app.modules.auth.service.session_service import create_session

from app.modules.auth.service.login_ticket_service import create_login_ticket


def handle_google_login(
    db: Session,
    code: str,
):
    """
    Full Google OAuth login pipeline.

    This is the SINGLE entry point for:
    - OAuth code exchange
    - ID token verification
    - user creation / lookup
    - JWT generation
    - session creation
    """

    # =========================
    # 1. Exchange code for tokens
    # =========================
    token_response = exchange_code_for_tokens(code)

    id_token_value = token_response.get("id_token")

    if not id_token_value:
        raise ValueError("Google did not return id_token")

    # =========================
    # 2. Verify ID token
    # =========================
    payload = verify_google_id_token(id_token_value)

    if not payload:
        raise ValueError("Invalid Google ID token")

    # =========================
    # 3. Get or create user
    # =========================
    user = get_or_create_google_user(db, payload)

    # =========================
    # 4. Create internal JWT tokens
    # =========================
    tokens = create_auth_tokens(
        user=user,
        remember_me=False
    )

    # =========================
    # 5. Create session
    # =========================
    create_session(
        db=db,
        user_id=user.id,
        decoded_refresh=tokens["decoded_refresh"],
        device_id=tokens["device_id"]
    )

    ticket = create_login_ticket(
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        user={
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "status": user.status,
            "profile_completed": user.profile_completed,
        },
    )

    return {
        "ticket": ticket,
    }