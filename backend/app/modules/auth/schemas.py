from pydantic import BaseModel, EmailStr, Field


# =========================
# REGISTER
# =========================
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=64
    )


# =========================
# VERIFY REGISTRATION
# =========================
class VerifyRegistrationRequest(BaseModel):
    email: EmailStr
    code: str = Field(
        min_length=6,
        max_length=6
    )


# =========================
# COMPLETE REGISTRATION
# =========================
class CompleteRegistrationRequest(BaseModel):
    email: EmailStr


# =========================
# RESEND REGISTRATION CODE
# =========================
class ResendRegistrationCodeRequest(BaseModel):
    email: EmailStr


# =========================
# LOGIN
# =========================
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    remember_me: bool = False
    device_id: str | None = None


# =========================
# REFRESH TOKEN REQUEST
# =========================
class RefreshTokenRequest(BaseModel):
    refresh_token: str


# =========================
# LOGOUT REQUEST
# =========================
class LogoutRequest(BaseModel):
    refresh_token: str


# =========================
# TOKEN RESPONSE
# =========================
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# =========================
# USER RESPONSE
# =========================
class UserOut(BaseModel):
    id: int
    full_name: str | None
    email: EmailStr


# =========================
# FORGOT PASSWORD
# =========================
class ForgotPasswordRequest(BaseModel):
    email: EmailStr


# =========================
# VERIFY RESET CODE
# =========================
class VerifyResetCodeRequest(BaseModel):
    email: EmailStr
    code: str = Field(
        min_length=6,
        max_length=6
    )


# =========================
# RESET PASSWORD
# =========================
class ResetPasswordRequest(BaseModel):
    email: EmailStr
    code: str = Field(
        min_length=6,
        max_length=6
    )
    new_password: str = Field(
        min_length=8,
        max_length=64
    )


class GoogleTicketRequest(BaseModel):
    ticket: str