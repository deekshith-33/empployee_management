import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from core.security import hash_password
from database.database import Base, get_db
from main import app
from models.models import Department, User

# Isolated in-memory SQLite database for testing
SQLALCHEMY_TEST_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    """Create fresh tables before each test and drop them afterward."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    # Seed one department and one admin user
    dept = Department(id=1, name="Engineering", description="Software Development")
    admin_user = User(
        email="admin@example.com",
        hashed_password=hash_password("AdminPass123"),
        role="admin",
    )
    db.add(dept)
    db.add(admin_user)
    db.commit()
    db.close()

    yield

    Base.metadata.drop_all(bind=engine)


def get_auth_headers(email: str, password: str) -> dict:
    res = client.post(
        "/users/login",
        data={"username": email, "password": password},
    )
    assert res.status_code == 200
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# ============================
# 1. AUTHENTICATION TESTS
# ============================

def test_register_and_login_employee():
    # Register new employee
    reg_res = client.post(
        "/users/register",
        json={"email": "john@example.com", "password": "Password123"},
    )
    assert reg_res.status_code == 201
    data = reg_res.json()
    assert data["email"] == "john@example.com"
    assert data["role"] == "employee"

    # Duplicate email should fail with 400
    dup_res = client.post(
        "/users/register",
        json={"email": "john@example.com", "password": "Password123"},
    )
    assert dup_res.status_code == 400

    # Login and fetch /users/me
    headers = get_auth_headers("john@example.com", "Password123")
    me_res = client.get("/users/me", headers=headers)
    assert me_res.status_code == 200
    assert me_res.json()["email"] == "john@example.com"


def test_login_invalid_credentials():
    res = client.post(
        "/users/login",
        data={"username": "admin@example.com", "password": "WrongPassword"},
    )
    assert res.status_code == 401


def test_protected_route_without_token():
    res = client.get("/employees/")
    assert res.status_code == 401


# ============================
# 2. EMPLOYEE CRUD & RBAC TESTS
# ============================

def test_admin_employee_crud_lifecycle():
    admin_headers = get_auth_headers("admin@example.com", "AdminPass123")

    # 1. Create employee (POST)
    create_res = client.post(
        "/employees/",
        headers=admin_headers,
        json={
            "first_name": "Alice",
            "last_name": "Sharma",
            "email": "alice@company.com",
            "salary": 75000.0,
            "department_id": 1,
        },
    )
    assert create_res.status_code == 201
    emp = create_res.json()
    emp_id = emp["id"]
    assert emp["first_name"] == "Alice"
    assert emp["department_name"] == "Engineering"

    # 2. Get employee by ID (GET)
    get_res = client.get(f"/employees/{emp_id}", headers=admin_headers)
    assert get_res.status_code == 200
    assert get_res.json()["email"] == "alice@company.com"

    # 3. Update employee (PUT)
    put_res = client.put(
        f"/employees/{emp_id}",
        headers=admin_headers,
        json={"salary": 85000.0},
    )
    assert put_res.status_code == 200
    assert put_res.json()["salary"] == 85000.0

    # 4. Delete employee (DELETE)
    del_res = client.delete(f"/employees/{emp_id}", headers=admin_headers)
    assert del_res.status_code == 204

    # 5. Confirm 404 after deletion
    not_found_res = client.get(f"/employees/{emp_id}", headers=admin_headers)
    assert not_found_res.status_code == 404
    assert not_found_res.json()["error_code"] == "EMPLOYEE_NOT_FOUND"


def test_employee_role_forbidden_from_write_actions():
    # Register a regular employee
    client.post(
        "/users/register",
        json={"email": "worker@company.com", "password": "Password123"},
    )
    emp_headers = get_auth_headers("worker@company.com", "Password123")

    # Employee CAN list employees
    list_res = client.get("/employees/", headers=emp_headers)
    assert list_res.status_code == 200

    # Employee CANNOT create a new employee (403 Forbidden)
    create_res = client.post(
        "/employees/",
        headers=emp_headers,
        json={
            "first_name": "Bob",
            "last_name": "Verma",
            "email": "bob@company.com",
            "salary": 50000.0,
            "department_id": 1,
        },
    )
    assert create_res.status_code == 403


def test_pagination_search_and_sorting():
    admin_headers = get_auth_headers("admin@example.com", "AdminPass123")

    employees_to_seed = [
        {"first_name": "Charlie", "last_name": "Nair", "email": "charlie@company.com", "salary": 60000, "department_id": 1},
        {"first_name": "Ananya", "last_name": "Rao", "email": "ananya@company.com", "salary": 90000, "department_id": 1},
        {"first_name": "Bharat", "last_name": "Kulkarni", "email": "bharat@company.com", "salary": 45000, "department_id": 1},
    ]
    for emp in employees_to_seed:
        res = client.post("/employees/", headers=admin_headers, json=emp)
        assert res.status_code == 201

    # Test search + sort by salary descending + pagination
    res = client.get(
        "/employees/?page=1&limit=2&sort_by=salary&order=desc",
        headers=admin_headers,
    )
    assert res.status_code == 200
    body = res.json()
    assert body["total"] == 3
    assert body["total_pages"] == 2
    assert len(body["items"]) == 2
    assert body["items"][0]["first_name"] == "Ananya"  # Highest salary first

    # Test search filter
    search_res = client.get("/employees/?search=bharat", headers=admin_headers)
    assert search_res.status_code == 200
    assert search_res.json()["total"] == 1
    assert search_res.json()["items"][0]["email"] == "bharat@company.com"