from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app.models.department import Department
from app.modules.departments.schemas import DepartmentCreate


def create_department(db: Session, payload: DepartmentCreate):

    dept = Department(name=payload.name)

    try:
        db.add(dept)
        db.commit()
        db.refresh(dept)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Department already exists"
        )

    return dept