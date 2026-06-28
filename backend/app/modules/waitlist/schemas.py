from pydantic import BaseModel


class WaitlistJoin(BaseModel):
    user_id: int
    department_id: int


class WaitlistOut(BaseModel):
    id: int
    status: str

    class Config:
        from_attributes = True