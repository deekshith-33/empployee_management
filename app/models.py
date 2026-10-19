from typing import Any, Dict


class User:
    """Base class representing a general system user."""

    def __init__(self, user_id: int, name: str, email: str) -> None:
        self.id: int = user_id
        self.name: str = name
        self.email: str = email


class Employee(User):
    """Employee entity extending User with department and salary."""

    def __init__(
        self,
        emp_id: int,
        name: str,
        email: str,
        department: str,
        salary: float,
    ) -> None:
        super().__init__(user_id=emp_id, name=name, email=email)
        self.department: str = department
        self._salary: float = salary

    @property
    def salary(self) -> float:
        return self._salary

    @salary.setter
    def salary(self, value: float) -> None:
        if value < 0:
            raise ValueError("Salary cannot be negative.")
        self._salary = value

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "department": self.department,
            "salary": self._salary,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Employee":
        return cls(
            emp_id=int(data["id"]),
            name=str(data["name"]),
            email=str(data["email"]),
            department=str(data["department"]),
            salary=float(data["salary"]),
        )