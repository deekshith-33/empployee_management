from typing import Literal, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from core.dependencies import get_current_user, require_admin
from database.database import get_db
from models.models import User
from schema.schema import (
    EmployeeCreate,
    EmployeeResponse,
    EmployeeUpdate,
    PaginatedEmployeeResponse,
)
import service

router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
)


@router.get("/", response_model=PaginatedEmployeeResponse)
def get_employees(
    page: int = Query(1, ge=1, description="Page number (starts at 1)"),
    limit: int = Query(10, ge=1, le=100, description="Items per page (max 100)"),
    search: Optional[str] = Query(None, description="Search by first name, last name, or email"),
    department_id: Optional[int] = Query(None, gt=0, description="Filter by department ID"),
    min_salary: Optional[float] = Query(None, ge=0, description="Minimum salary filter"),
    max_salary: Optional[float] = Query(None, ge=0, description="Maximum salary filter"),
    sort_by: str = Query("id", description="Sort field: id, first_name, last_name, email, salary, created_at"),
    order: Literal["asc", "desc"] = Query("asc", description="Sort direction: asc or desc"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Any authenticated user can list employees with pagination, filtering, sorting, and search."""
    return service.get_all_employees(
        db=db,
        page=page,
        limit=limit,
        search=search,
        department_id=department_id,
        min_salary=min_salary,
        max_salary=max_salary,
        sort_by=sort_by,
        order=order,
    )


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Admins can view any employee; regular employees can only view their own profile."""
    employee = service.get_employee_by_id(employee_id, db)

    if current_user.role != "admin" and employee.get("user_id") != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are only authorized to view your own employee record.",
        )

    return employee


@router.post("/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(
    payload: EmployeeCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    """Only admins can create new employees."""
    return service.create_new_employee(payload, db)


@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    payload: EmployeeUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    """Only admins can update employee records."""
    return service.update_existing_employee(employee_id, payload, db)


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    """Only admins can delete employees."""
    service.delete_existing_employee(employee_id, db)