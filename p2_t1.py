# 1. List & Filter Employees
#  Method: GET /employees
#  Query Params: ?department=string (optional) & search=string (optional)
#  Success Code: 200 OK
#  Response: [{"id": 1, "name": "Rajesh", "email": "rajesh@company.com", "department": "IT", "salary": 
# 75000.0}]


# 2. Get Single Employee by ID
#  Method: GET /employees/{employee_id}
#  Path Param: employee_id (integer, required)
#  Success Code: 200 OK
#  Error Code: 404 Not Found


# 3. Create New Employee
#  Method: POST /employees
#  Header: Content-Type: application/json
#  Request Body: {"name": "Bob", "email": "bob@company.com", "department": "HR", "salary": 62000.0}
#  Success Code: 201 Created
#  Error Code: 409 Conflict (Email duplicate) / 422 Unprocessable (Validation error)


# 4. Update Existing Employee
#  Method: PUT /employees/{employee_id}
#  Path Param: employee_id (integer, required)
#  Request Body: {"name": "Bob Smith", "email": "bob.smith@company.com", "department": "HR", "salary": 
# 68000.0}
#  Success Code: 200 OK
#  Error Code: 404 Not Found


# 5. Delete Employee
#  Method: DELETE /employees/{employee_id}
#  Path Param: employee_id (integer, required)
#  Success Code: 200 OK or 204 No Content
#  Error Code: 404 Not Found
# ==============================