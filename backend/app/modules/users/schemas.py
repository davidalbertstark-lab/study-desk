from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: str
    password: str
    device_id: str | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    remember_me: bool = False
    device_id: str | None = None


class UserOut(BaseModel):
    id: int
    full_name: str | None
    email: EmailStr

    class Config:
        from_attributes = True


class CompleteProfileRequest(BaseModel):
    full_name: str
    matric_number: str
    level: str
    faculty: str
    department: str