
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, status

from schema.schema import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse,
)

app = FastAPI(
    title="Employee Management API",
    version="1.0.0",
)


# In-memory database for employees

EMPLOYEES_DB: List[Dict] = [
    {
        "id": 1,
        "name": "Rajesh",
        "email": "rajesh@company.com",
        "department": "IT",
        "salary": 75000.0,
    },
    {
        "id": 2,
        "name": "Nagesh",
        "email": "nagesh@company.com",
        "department": "HR",
        "salary": 62000.0,
    },
    {
        "id": 3,
        "name": "Suresh",
        "email": "suresh@company.com",
        "department": "Finance",
        "salary": 70000.0,
    },
]


# GET: Retrieve all employees, with optional filters

@app.get(
    "/employees",
    response_model=List[EmployeeResponse],
    tags=["Employees"],
    status_code=status.HTTP_200_OK,
)
def get_employees(
    department: Optional[str] = None,
    search: Optional[str] = None,
) -> List[EmployeeResponse]:

    results = EMPLOYEES_DB

    if department:
        results = [
            e for e in results
            if e["department"].lower() == department.lower()
        ]

    if search:
        s = search.lower()
        results = [
            e for e in results
            if s in e["name"].lower()
            or s in e["email"].lower()
        ]

    return results


# GET: Retrieve one employee by ID

@app.get(
    "/employees/{employee_id}",
    response_model=EmployeeResponse,
    tags=["Employees"],
    status_code=status.HTTP_200_OK,
)
def get_employee_by_id(employee_id: int) -> EmployeeResponse:

    for emp in EMPLOYEES_DB:
        if emp["id"] == employee_id:
            return emp

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Employee with ID {employee_id} was not found.",
    )


# POST: Create a new employee

@app.post(
    "/employees",
    response_model=EmployeeResponse,
    tags=["Employees"],
    status_code=status.HTTP_201_CREATED,
)
def create_employee(payload: EmployeeCreate) -> EmployeeResponse:

    # Check for duplicate email
    email = str(payload.email).strip().lower()

    if any(e["email"].lower() == email for e in EMPLOYEES_DB):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"An employee with email '{payload.email}' already exists.",
        )

    # Generate the next employee ID
    next_id = max(
        (e["id"] for e in EMPLOYEES_DB),
        default=0,
    ) + 1

    # Convert Pydantic model into a dictionary
    employee_data = payload.model_dump()

    # Clean text fields
    employee_data["name"] = employee_data["name"].strip()
    employee_data["email"] = str(payload.email).strip()
    employee_data["department"] = employee_data["department"].strip()

    new_employee = {
        "id": next_id,
        **employee_data,
    }

    EMPLOYEES_DB.append(new_employee)

    return new_employee


# PUT: Update an existing employee

@app.put(
    "/employees/{employee_id}",
    response_model=EmployeeResponse,
    tags=["Employees"],
    status_code=status.HTTP_200_OK,
)
def update_employee(
    employee_id: int,
    payload: EmployeeUpdate,
) -> EmployeeResponse:

    target = next(
        (e for e in EMPLOYEES_DB if e["id"] == employee_id),
        None,
    )

    if not target:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {employee_id} was not found.",
        )

    # Include only fields supplied by the client.
    # Ignore explicit null values in this implementation.
    update_data = {
        key: value
        for key, value in payload.model_dump(exclude_unset=True).items()
        if value is not None
    }

    # Check for duplicate email
    if "email" in update_data:
        new_email = str(update_data["email"]).strip().lower()

        if any(
            e["email"].lower() == new_email
            and e["id"] != employee_id
            for e in EMPLOYEES_DB
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An employee with this email already exists.",
            )

        update_data["email"] = str(update_data["email"]).strip()

    # Clean provided text fields
    if "name" in update_data:
        update_data["name"] = update_data["name"].strip()

    if "department" in update_data:
        update_data["department"] = update_data["department"].strip()

    # Apply the validated changes
    target.update(update_data)

    return target


# DELETE: Remove an employee

@app.delete(
    "/employees/{employee_id}",
    tags=["Employees"],
    status_code=status.HTTP_200_OK,
)
def delete_employee(employee_id: int) -> Dict[str, str]:

    global EMPLOYEES_DB

    existing = next(
        (e for e in EMPLOYEES_DB if e["id"] == employee_id),
        None,
    )

    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {employee_id} does not exist.",
        )

    EMPLOYEES_DB = [
        e for e in EMPLOYEES_DB
        if e["id"] != employee_id
    ]

    return {
        "message": f"Employee with ID {employee_id} was successfully deleted."
    }
