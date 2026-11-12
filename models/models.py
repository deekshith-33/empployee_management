from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    Text,
    ForeignKey,
    CheckConstraint,
    DateTime,
    text,
)
from sqlalchemy.orm import relationship

from database.database import Base


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)

    created_at = Column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
    )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(
        String(50),
        nullable=False,
        server_default="employee",
    )

    employee = relationship("Employee", back_populates="user", uselist=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
    )


class Employee(Base):
    __tablename__ = "employees"

    __table_args__ = (
        CheckConstraint(
            "salary > 0",
            name="employees_salary_check",
        ),
    )

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    salary = Column(Numeric(10, 2), nullable=False)

    department_id = Column(
        Integer,
        ForeignKey("departments.id", ondelete="RESTRICT"),
        nullable=False,
    )
    department = relationship("Department")

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        unique=True,
        nullable=True,
    )
    user = relationship("User", back_populates="employee")

    created_at = Column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
    )