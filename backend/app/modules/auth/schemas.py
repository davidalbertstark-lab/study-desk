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
# OPTIONAL: USER RESPONSE SHAPE (VERY USEFUL NEXT STEP)
# =========================
class UserOut(BaseModel):
    id: int
    full_name: str | None
    email: EmailStr