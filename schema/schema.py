
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class EmployeeBase(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    salary: float = Field(..., gt=0)
    department_id: int = Field(..., gt=0)


class EmployeeCreate(EmployeeBase):
    user_id: Optional[int] = Field(None, gt=0)


class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=2, max_length=100)
    last_name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    salary: Optional[float] = Field(None, gt=0)
    department_id: Optional[int] = Field(None, gt=0)
    user_id: Optional[int] = Field(None, gt=0)


class EmployeeResponse(EmployeeBase):
    id: int
    department_name: str

    model_config = ConfigDict(from_attributes=True)
