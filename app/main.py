from app.logger import logger
from app.service import EmployeeService


def display_employees(employees) -> None:
    if not employees:
        print("No employee records found.")
        return

    print(f"\n{'ID':<6}{'Name':<20}{'Email':<30}{'Department':<15}{'Salary':<10}")
    print("-" * 81)
    for emp in employees:
        print(
            f"{emp.id:<6}{emp.name:<20}{emp.email:<30}{emp.department:<15}{emp.salary:<10.2f}"
        )


def main() -> None:
    logger.info("Employee Management CLI started")
    service = EmployeeService()

    while True:
        print("\n===============================")
        print("   EMPLOYEE MANAGEMENT SYSTEM  ")
        print("===============================")
        print("1. List All Employees")
        print("2. Add Employee")
        print("3. Search Employee")
        print("4. Delete Employee")
        print("5. Exit")

        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            display_employees(service.get_all())

        elif choice == "2":
            name = input("Enter Name: ").strip()
            email = input("Enter Email: ").strip()
            dept = input("Enter Department: ").strip()
            try:
                salary = float(input("Enter Salary: ").strip())
                new_emp = service.create(name, email, dept, salary)
                print(f"Success: Employee created with ID: {new_emp.id}")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "3":
            query = input("Enter search term: ").strip()
            display_employees(service.search(query))

        elif choice == "4":
            try:
                emp_id = int(input("Enter Employee ID to delete: ").strip())
                if service.delete(emp_id):
                    print("Employee deleted successfully.")
                else:
                    print(f"Employee ID {emp_id} not found.")
            except ValueError:
                print("Error: Invalid ID.")

        elif choice == "5":
            logger.info("Application closed by user")
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()