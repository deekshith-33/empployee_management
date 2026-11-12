import math
from typing import Optional
from sqlalchemy import asc, desc, or_
from sqlalchemy.orm import Session

from core.exceptions import (
    DatabaseOperationException,
    DepartmentNotFoundException,
    DuplicateEmailException,
    EmployeeNotFoundException,
    InvalidSortFieldException,
)
from core.logging_config import logger
from models.models import Department, Employee
from schema.schema import EmployeeCreate, EmployeeUpdate

ALLOWED_SORT_FIELDS = {
    "id": Employee.id,
    "first_name": Employee.first_name,
    "last_name": Employee.last_name,
    "email": Employee.email,
    "salary": Employee.salary,
    "created_at": Employee.created_at,
}


def employee_to_dict(employee: Employee) -> dict:
    return {
        "id": employee.id,
        "first_name": employee.first_name,
        "last_name": employee.last_name,
        "email": employee.email,
        "salary": float(employee.salary),
        "department_id": employee.department_id,
        "department_name": employee.department.name if employee.department else "Unknown",
        "user_id": employee.user_id,
    }


def get_all_employees(
    db: Session,
    page: int = 1,
    limit: int = 10,
    search: Optional[str] = None,
    department_id: Optional[int] = None,
    min_salary: Optional[float] = None,
    max_salary: Optional[float] = None,
    sort_by: str = "id",
    order: str = "asc",
) -> dict:
    if sort_by not in ALLOWED_SORT_FIELDS:
        raise InvalidSortFieldException(sort_by, list(ALLOWED_SORT_FIELDS.keys()))

    query = db.query(Employee)

    # 1. Search across first_name, last_name, or email (case-insensitive)
    if search:
        pattern = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Employee.first_name.ilike(pattern),
                Employee.last_name.ilike(pattern),
                Employee.email.ilike(pattern),
            )
        )

    # 2. Filtering
    if department_id is not None:
        query = query.filter(Employee.department_id == department_id)
    if min_salary is not None:
        query = query.filter(Employee.salary >= min_salary)
    if max_salary is not None:
        query = query.filter(Employee.salary <= max_salary)

    # 3. Total count before pagination
    total = query.count()

    # 4. Sorting
    sort_column = ALLOWED_SORT_FIELDS[sort_by]
    query = query.order_by(desc(sort_column) if order.lower() == "desc" else asc(sort_column))

    # 5. Pagination
    offset = (page - 1) * limit
    employees = query.offset(offset).limit(limit).all()
    total_pages = math.ceil(total / limit) if total > 0 else 1

    logger.info(
        "Fetched paginated employees",
        extra={
            "extra_data": {
                "page": page,
                "limit": limit,
                "total": total,
                "search": search,
                "department_id": department_id,
                "sort_by": sort_by,
                "order": order,
            }
        },
    )

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "items": [employee_to_dict(emp) for emp in employees],
    }


def get_employee_by_id(employee_id: int, db: Session) -> dict:
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if employee is None:
        raise EmployeeNotFoundException(employee_id)
    return employee_to_dict(employee)


def create_new_employee(payload: EmployeeCreate, db: Session) -> dict:
    existing = db.query(Employee).filter(Employee.email == str(payload.email)).first()
    if existing:
        raise DuplicateEmailException(str(payload.email))

    department = db.query(Department).filter(Department.id == payload.department_id).first()
    if not department:
        raise DepartmentNotFoundException(payload.department_id)

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
        logger.info("Created employee", extra={"extra_data": {"employee_id": employee.id, "email": employee.email}})
        return employee_to_dict(employee)
    except Exception as exc:
        db.rollback()
        logger.error("Failed to create employee", exc_info=True)
        raise DatabaseOperationException("Could not create employee due to a database constraint.") from exc


def update_existing_employee(employee_id: int, payload: EmployeeUpdate, db: Session) -> dict:
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if employee is None:
        raise EmployeeNotFoundException(employee_id)

    changes = payload.model_dump(exclude_unset=True)

    if "email" in changes:
        changes["email"] = str(changes["email"])
        duplicate = (
            db.query(Employee)
            .filter(Employee.email == changes["email"], Employee.id != employee_id)
            .first()
        )
        if duplicate:
            raise DuplicateEmailException(changes["email"])

    if "department_id" in changes:
        department = db.query(Department).filter(Department.id == changes["department_id"]).first()
        if not department:
            raise DepartmentNotFoundException(changes["department_id"])

    allowed_fields = {"first_name", "last_name", "email", "salary", "department_id", "user_id"}
    for field, value in changes.items():
        if field in allowed_fields:
            setattr(employee, field, value)

    try:
        db.commit()
        db.refresh(employee)
        logger.info("Updated employee", extra={"extra_data": {"employee_id": employee.id}})
        return employee_to_dict(employee)
    except Exception as exc:
        db.rollback()
        logger.error("Failed to update employee", exc_info=True)
        raise DatabaseOperationException("Could not update employee due to a database constraint.") from exc


def delete_existing_employee(employee_id: int, db: Session) -> None:
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if employee is None:
        raise EmployeeNotFoundException(employee_id)

    db.delete(employee)
    db.commit()
    logger.info("Deleted employee", extra={"extra_data": {"employee_id": employee_id}})