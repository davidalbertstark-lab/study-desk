from sqlalchemy import Column, Integer, ForeignKey
from app.db.base import Base


class DepartmentLeader(Base):
    __tablename__ = "department_leaders"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), index=True, nullable=False)

    role = Column(String, default="leader")
    # leader | sub_leader