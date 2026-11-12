from fastapi import FastAPI
from routes.employee_routes import router as employee_router
from routes import auth

app = FastAPI(
    title="Employee Management API",
    description="Employee management using FastAPI and PostgreSQL",
    version="1.0.0"
)


app.include_router(auth.router)
app.include_router(employee_router)


@app.get("/")
def home():
    return {
        "message": "Employee Management API is running"
    }