from fastapi import FastAPI
from fastapi.responses import JSONResponse
from routes.employee_routes import router as employee_router
from routes import auth
from fastapi import FastAPI, HTTPException, Request

app = FastAPI(
    title="Employee Management API",
    description="Employee management using FastAPI and PostgreSQL",
    version="1.0.0"
)


app.include_router(auth.router)
app.include_router(employee_router)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    error_code = getattr(exc, "error_code", "HTTP_ERROR")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error_code": error_code,
            "message": exc.detail,
            "path": request.url.path,
        },
    )


@app.get("/")
def home():
    return {
        "message": "Employee Management API is running"
    }