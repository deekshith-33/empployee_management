
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.database import get_db

from database.database import get_db
from models.models import Employee
from schema.schema import EmployeeCreate, EmployeeUpdate

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


def employee_to_dict(employee: Employee):
    return {
        "id": employee.id,
        "first_name": employee.first_name,
        "last_name": employee.last_name,
        "email": employee.email,
        "salary": float(employee.salary),
        "department_name": employee.department.name,
    }

@router.get("/")
def get_employees(db: Session = Depends(get_db)):
    employees = db.query(Employee).all()
    return [employee_to_dict(emp) for emp in employees]


@router.get("/{employee_id}")
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    return employee_to_dict(employee)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_employee(
    payload: EmployeeCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(Employee).filter(
        Employee.email == payload.email
    ).first()

    if existing:
        raise HTTPException(status_code=409, detail="Email already exists")

    employee = Employee(
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=str(payload.email),
        salary=payload.salary,
        department_id=payload.department_id,
        user_id=payload.user_id,
    )

    try:
        db.add(employee)
        db.commit()
        db.refresh(employee)
        return employee_to_dict(employee)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not create employee")


@router.put("/{employee_id}")
def update_employee(
    employee_id: int,
    payload: EmployeeUpdate,
    db: Session = Depends(get_db)
):
    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    changes = payload.model_dump(exclude_unset=True)

    if "email" in changes:
        changes["email"] = str(changes["email"])

        duplicate = db.query(Employee).filter(
            Employee.email == changes["email"],
            Employee.id != employee_id
        ).first()

        if duplicate:
            raise HTTPException(status_code=409, detail="Email already exists")

    for field, value in changes.items():
        if field in {"first_name", "last_name", "email", "salary", "department_id", "user_id"}:
            setattr(employee, field, value)

    try:
        db.commit()
        db.refresh(employee)
        return employee_to_dict(employee)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not update employee")


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(employee)
    db.commit()
