class AuthException(Exception):
    """
    Base exception for all authentication-related errors.
    """
    def __init__(self, message: str = "Authentication error", code: str = "AUTH_ERROR"):
        self.message = message
        self.code = code
        super().__init__(message)


# =========================
# AUTH FAILURES
# =========================

class InvalidCredentialsError(AuthException):
    def __init__(self):
        super().__init__(
            message="Invalid email or password",
            code="INVALID_CREDENTIALS"
        )


class UserNotFoundError(AuthException):
    def __init__(self):
        super().__init__(
            message="User not found",
            code="USER_NOT_FOUND"
        )


class AccountNotActiveError(AuthException):
    def __init__(self, status: str):
        super().__init__(
            message=f"Account not active: {status}",
            code="ACCOUNT_NOT_ACTIVE"
        )


# =========================
# TOKEN ERRORS
# =========================

class InvalidTokenError(AuthException):
    def __init__(self):
        super().__init__(
            message="Invalid or malformed token",
            code="INVALID_TOKEN"
        )


class ExpiredTokenError(AuthException):
    def __init__(self):
        super().__init__(
            message="Token expired or revoked",
            code="EXPIRED_TOKEN"
        )


# =========================
# SESSION ERRORS
# =========================

class SessionNotFoundError(AuthException):
    def __init__(self):
        super().__init__(
            message="Session expired or revoked",
            code="SESSION_NOT_FOUND"
        )


class SessionRotationError(AuthException):
    def __init__(self):
        super().__init__(
            message="Failed to rotate session",
            code="SESSION_ROTATION_FAILED"
        )


# =========================
# REGISTRATION ERRORS
# =========================

class RegistrationVerificationError(AuthException):
    def __init__(self):
        super().__init__(
            message="Invalid or expired verification code",
            code="REGISTRATION_VERIFICATION_FAILED"
        )


class PasswordResetError(AuthException):
    def __init__(self):
        super().__init__(
            message="Password reset failed or invalid code",
            code="PASSWORD_RESET_FAILED"
        )



class InvalidLoginTicketError(AuthException):
    def __init__(self):
        super().__init__(
            message="Invalid or expired login ticket",
            code="INVALID_LOGIN_TICKET",
        )