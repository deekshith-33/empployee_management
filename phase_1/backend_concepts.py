import asyncio
import time
from contextlib import contextmanager
from functools import wraps
from typing import Any, Callable, Generator, Optional,List,Union,Dict
from unittest import result

#1 Type Hints

def find_employee(
    emp_id: int,
    department_filter: Optional[str] = None,
) -> Union[Dict[str, Any], str]:

    sample_employees = {
        101: {"id": 1, "name": "Akash", "department": "HR"},
        102: {"id": 2, "name": "Ranjith", "department": "IT"},
        103: {"id": 3, "name": "Suresh", "department": "Finance"},
    }

    employee = sample_employees.get(emp_id)
    if not employee:
        return "Employee not found"

    if department_filter and employee["department"].lower() != department_filter.lower():
        return "Employee not found in the specified department"

    return employee

#2 Custom Decorator

def execution_logger(func: Callable)-> Callable:
    """Decorator that measures execution time and logs function calls."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.perf_counter()
        print(f"\n[DECORATOR] Invoking '{func.__name__}'...")
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start_time
        print(f"[DECORATOR] '{func.__name__}' executed in {duration:.4f} seconds")
        return result

    return wrapper

@execution_logger
def calculate_payroll(salaries: List[float]) -> float:
    time.sleep(0.1)
    return sum(salaries)


async def fetch_employee_audit_log(emp_id: int) -> Dict[str, Any]:
    print(f"[ASYNC] Fetching audit log for employee ID {emp_id}...")
    await asyncio.sleep(1.0)
    print(f"[ASYNC] Audit log fetched for employee ID {emp_id}")
    return {"emp_id": emp_id, "Status": "Audit log fetched successfully"}


async def run_async_tasks() -> None:
    print("\n---Starting Asynchronous Task---")
    start_time = time.perf_counter()

    result = await asyncio.gather(
        fetch_employee_audit_log(101),
        fetch_employee_audit_log(102),
    )

    elapsed = time.perf_counter() - start_time
    print(f"[ASYNC] All tasks completed in {elapsed:.2f} seconds")


#4 Gnerators and Context Managers

@contextmanager
def get_db_session() -> Generator[str, None, None]:
    session_id = "Session 12345"
    print(f"\n[CONTEXT MANAGER] Opening DB session: {session_id}")
    try:
        yield session_id
    finally:
        print(f"[CONTEXT MANAGER] Closing DB session: {session_id}")


def main() -> None:
    # 1. Type Hints
    print("--- 1. Testing Type Hints & Union ---")
    print(find_employee(101))
    print(find_employee(101, department_filter="Finance"))
    print(find_employee(999))

    # 2. Decorators
    print("\n--- 2. Testing Custom Decorator ---")
    total = calculate_payroll([45000.0, 62000.0, 78000.0])
    print(f"Total Payroll: ${total:,.2f}")

    # 3. Context Manager / Generator
    print("\n--- 3. Testing Context Manager / Generator ---")
    with get_db_session() as session:
        print(f"Executing SQL queries inside active connection: {session}")

    # 4. Async / Await
    print("\n--- 4. Testing Async / Await ---")
    asyncio.run(run_async_tasks())


if __name__ == "__main__":
    main()