import json
import os
from typing import List, Optional

from app.config import config
from app.logger import logger
from app.models import Employee


class EmployeeService:
    """Service handling CRUD operations and JSON persistence."""

    def __init__(self) -> None:
        self.file_path = config.DATA_FILE
        self._ensure_storage()

    def _ensure_storage(self) -> None:
        os.makedirs(self.file_path.parent, exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4)
            logger.info(f"Initialized storage file at: {self.file_path}")

    def get_all(self) -> List[Employee]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
                return [Employee.from_dict(item) for item in raw_data]
        except (json.JSONDecodeError, IOError) as err:
            logger.error(f"Error reading employees: {err}")
            return []

    def save_all(self, employees: List[Employee]) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            data = [emp.to_dict() for emp in employees]
            json.dump(data, f, indent=4)
            f.flush()
            os.fsync(f.fileno())

    def create(self, name: str, email: str, department: str, salary: float) -> Employee:
        employees = self.get_all()

        if any(e.email.lower() == email.lower() for e in employees):
            logger.warning(f"Attempted duplicate registration for email: {email}")
            raise ValueError(f"Email '{email}' is already registered.")

        next_id = max((e.id for e in employees), default=0) + 1
        new_emp = Employee(next_id, name, email, department, salary)
        employees.append(new_emp)
        self.save_all(employees)

        logger.info(f"Created new employee ID {new_emp.id} ({new_emp.name})")
        return new_emp

    def search(self, query: str) -> List[Employee]:
        query = query.lower()
        results = [
            e
            for e in self.get_all()
            if query in e.name.lower()
            or query in e.email.lower()
            or query in e.department.lower()
        ]
        logger.debug(f"Search query '{query}' matched {len(results)} record(s)")
        return results

    def delete(self, emp_id: int) -> bool:
        employees = self.get_all()
        filtered = [e for e in employees if e.id != emp_id]

        if len(filtered) == len(employees):
            logger.warning(f"Delete failed: Employee ID {emp_id} not found")
            return False

        self.save_all(filtered)
        logger.info(f"Deleted employee ID {emp_id}")
        return True
    