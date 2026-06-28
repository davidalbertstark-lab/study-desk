from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.departments.schemas import DepartmentCreate, DepartmentOut
from app.modules.departments.service import create_department
from app.core.responses import success_response

router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)


@router.post("/")
def create(
    payload: DepartmentCreate,
    db: Session = Depends(get_db)
):

    dept = create_department(db, payload)

    return success_response(
        data={
            "id": dept.id,
            "name": dept.name
        },
        message="department created"
    )