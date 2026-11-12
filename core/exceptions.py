class AppBaseException(Exception):
    """Base exception for all custom application errors."""
    def __init__(self, message: str, status_code: int = 400, error_code: str = "APP_ERROR"):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.message)


class EmployeeNotFoundException(AppBaseException):
    def __init__(self, employee_id: int):
        super().__init__(
            message=f"Employee with ID {employee_id} was not found.",
            status_code=404,
            error_code="EMPLOYEE_NOT_FOUND",
        )


class DepartmentNotFoundException(AppBaseException):
    def __init__(self, department_id: int):
        super().__init__(
            message=f"Department with ID {department_id} does not exist.",
            status_code=404,
            error_code="DEPARTMENT_NOT_FOUND",
        )


class DuplicateEmailException(AppBaseException):
    def __init__(self, email: str):
        super().__init__(
            message=f"An employee with email '{email}' already exists.",
            status_code=409,
            error_code="DUPLICATE_EMAIL",
        )


class InvalidSortFieldException(AppBaseException):
    def __init__(self, sort_by: str, allowed_fields: list[str]):
        super().__init__(
            message=f"Invalid sort field '{sort_by}'. Allowed fields: {', '.join(allowed_fields)}.",
            status_code=400,
            error_code="INVALID_SORT_FIELD",
        )


class DatabaseOperationException(AppBaseException):
    def __init__(self, message: str = "Database operation failed."):
        super().__init__(
            message=message,
            status_code=400,
            error_code="DATABASE_OPERATION_ERROR",
        )