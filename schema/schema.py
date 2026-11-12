from datetime import datetime
from typing import List, Optional
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
    user_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class PaginatedEmployeeResponse(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int
    items: List[EmployeeResponse]


class UserBase(BaseModel):
    email: EmailStr
    role: str = "employee"


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=128)


class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --- Auth & Token Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None