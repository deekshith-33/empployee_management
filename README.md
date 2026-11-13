<<<<<<< HEAD
# Employee Management System

## Setup Instructions

1. **Create and Activate Virtual Environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
=======

# Employee Management System

A Python-based Employee Management System developed in two phases, progressing from a command-line application to a RESTful backend API with PostgreSQL database integration.

## Project Overview

The main objective of this project is to understand and implement employee management operations using Python and modern backend development technologies.

The project is divided into two phases:

- **Phase 1:** Command-Line Employee Management System using Python and JSON.
- **Phase 2:** RESTful Employee Management API using FastAPI and PostgreSQL.

---

# Phase 1 – Python CLI Employee Management System

## Description

Phase 1 focuses on developing a command-line application that allows users to manage employee records using Python.

Employee information is stored in a JSON file, allowing data to persist even after the application is closed.

## Features

- Add new employee records.
- View all employees.
- Search employees using Employee ID.
- Update existing employee details.
- Delete employee records.
- Validate employee information.
- Prevent duplicate email addresses.
- Validate employee IDs and salary values.
- Store employee data in a JSON file.
- Interactive menu-driven command-line interface.

## Employee Information

Each employee record contains:

| Field | Description |
|---|---|
| ID | Unique employee identifier |
| Name | Employee name |
| Email | Employee email address |
| Department | Employee department |
| Salary | Employee salary |

## Technologies Used

- Python
- JSON
- File Handling
- Functions
- Exception Handling
- Data Validation


---

# Phase 2 – FastAPI Employee Management REST API

## Description

Phase 2 upgrades the command-line application into a RESTful backend application using FastAPI.

Instead of interacting through a command-line menu, clients can communicate with the application through HTTP requests.

The application uses PostgreSQL for database storage and SQLAlchemy for database operations. Pydantic is used for request and response validation, while Alembic is used for database migrations.

## Features

- Develop RESTful APIs using FastAPI.
- Create employee records.
- Retrieve all employee records.
- Retrieve an employee using their ID.
- Update employee information.
- Delete employee records.
- Validate incoming request data using Pydantic.
- Connect FastAPI with PostgreSQL.
- Perform database operations using SQLAlchemy.
- Manage database schema changes using Alembic.
- Generate interactive API documentation using Swagger UI.
- Configure database credentials using environment variables.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| FastAPI | REST API development |
| PostgreSQL | Relational database |
| SQLAlchemy | ORM and database operations |
| Pydantic | Data validation and serialization |
| Alembic | Database migrations |
| Uvicorn | ASGI server |
| python-dotenv | Environment variable management |

## API Endpoints

Base URL: `http://127.0.0.1:8000`

| HTTP Method | Endpoint | Description |
|---|---|---|
| GET | `/employees/` | Retrieve all employees |
| GET | `/employees/{employee_id}` | Retrieve an employee by ID |
| POST | `/employees/` | Create a new employee |
| PUT | `/employees/{employee_id}` | Update an employee |
| DELETE | `/employees/{employee_id}` | Delete an employee |

*The endpoint list describes the intended employee CRUD API. Refer to the actual route definitions for the final endpoint paths and supported methods.*

## API Documentation

FastAPI automatically generates interactive API documentation.

After starting the application, open:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

You can test API endpoints directly from Swagger UI.

## Project Structure

```text
Emp_Mgmt/
├── core/
│   ├── dependencies.py      # JWT validation & RBAC role dependencies
│   ├── exceptions.py        # Custom domain exceptions
│   ├── logging_config.py    # Structured JSON logger
│   └── security.py          # Bcrypt password hashing & JWT utilities
├── database/
│   └── database.py          # SQLAlchemy engine & session dependency
├── models/
│   └── models.py            # Department, User, and Employee ORM models
├── postman/
│   └── Employee_Management_API.postman_collection.json
├── routes/
│   ├── auth.py              # Registration, login, and profile routes
│   └── employee_routes.py   # Protected Employee CRUD routes
├── schema/
│   └── schema.py            # Pydantic request/response schemas
├── tests/
│   └── test_api.py          # Automated pytest suite
├── main.py                  # FastAPI app, middleware & global error handlers
└── service.py               # Business logic, pagination, filtering & sorting
```

*The structure is illustrative. Keep the folder and file names synchronized with your actual project.*

---

# Installation and Setup

## 1. Clone the Repository

```bash
git clone <your-repository-url>
cd Emp_Mgmt
```

## 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure Environment Variables

Create a `.env` file in the project root directory.

Example:

```env
DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/employee_management
```

Replace the username and password with your PostgreSQL credentials.

Never upload your actual `.env` file or database passwords to GitHub.

## 5. Run Database Migrations

```bash
alembic upgrade head
```

## 6. Start the FastAPI Application

```bash
python -m uvicorn main:app --reload"
```

The application will run at:

```text
http://127.0.0.1:8000
```

---

# Learning Outcomes

Through this project, I gained practical experience with:

- Python programming and file handling.
- CRUD operations and data validation.
- Building RESTful APIs.
- HTTP methods and status codes.
- FastAPI application structure.
- Pydantic models and request validation.
- SQLAlchemy ORM and database connectivity.
- PostgreSQL database management.
- Database migrations using Alembic.
- Environment variable configuration.
- Testing APIs using Swagger UI.





---



---

*This project is being developed incrementally as part of my backend development learning journey.*
>>>>>>> 
