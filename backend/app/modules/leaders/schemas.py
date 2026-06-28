from pydantic import BaseModel
from datetime import datetime


class WaitlistUserOut(BaseModel):
    id: int
    user_id: int
    department_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True