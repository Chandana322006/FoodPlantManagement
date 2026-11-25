# Food Plant Operations Management System
## User Manual

### 1. Introduction

The Food Plant Operations Management System is a Python-based application developed using FastAPI. It helps manage production activities, raw materials, suppliers, machines, quality testing, approvals, and reports in a food manufacturing plant.

The application provides centralized data management, CSV imports, role-based authentication, and audit logging.

### 2. Technologies Used

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Pytest
- ReportLab

### 3. Starting the Application

1. Open the project folder in Visual Studio Code.
2. Open the terminal.
3. Activate the virtual environment:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

4. Start the application:

   ```powershell
   uvicorn app.main:app --reload
   ```

5. Open the API documentation in a browser:

   http://127.0.0.1:8000/docs

### 4. Authentication

The application provides login functionality and authenticated API access.

1. Open the `/auth/login` endpoint.
2. Enter the registered username and password.
3. Execute the request to receive an access token.
4. Click the **Authorize** button in Swagger UI.
5. Enter the bearer token as instructed by the authorization dialog.

Protected endpoints require valid authentication and appropriate role permissions.

### 5. Master Data Management

The application provides endpoints to manage:

- Products
- Production lines
- Suppliers
- Raw materials
- Machines
- Users
- Roles

Users can create and retrieve master data through the corresponding API endpoints.

### 6. Production Management

The system supports:

- Creating and retrieving production batches.
- Recording production input and output quantities.
- Recording wastage quantities.
- Storing optional moisture readings.
- Tracking production records.

### 7. Material Usage Management

The material usage module records raw materials consumed during production.

It checks material availability before recording usage and deducts the consumed quantity from available stock.

### 8. Quality Management

The quality testing module allows users to:

- Record quality tests for production batches.
- Store test dates and results.
- Add remarks.
- Retrieve quality test records.

### 9. Approval Management

The approval module supports batch approval workflows.

Users can create approval records and update approval status. The corresponding batch status is also updated.

### 10. CSV Import Management

The system supports importing historical data through CSV files for:

- Production records
- Raw materials
- Machines
- Quality tests
- Production batches

**Import procedure:**

1. Open the required CSV import endpoint in Swagger UI.
2. Click **Try it out**.
3. Select the CSV file.
4. Click **Execute**.
5. Review the import summary.

The import process validates records and reports successful and rejected rows with reasons.

### 11. Reports

The reporting module provides:

- Total production input.
- Total production output.
- Total wastage.
- Production yield percentage.
- Wastage percentage.
- Total quality tests.
- Rejected quality tests.
- Quality rejection rate.

### 12. Report Export

The application supports exporting reports in:

- CSV format
- PDF format

Users can execute the corresponding export endpoints in Swagger UI and download the generated reports.

### 13. Audit Logging

The audit logging module maintains records of selected system activities.

Audit records contain:

- User ID
- Action performed
- Entity type
- Entity ID
- Activity details
- Timestamp

Automatic audit logging is implemented for selected operations, including batch creation, production record creation, material usage, quality test creation, approval updates, and CSV imports.

### 14. Testing

The application uses Pytest for automated testing.

Run the complete test suite:

```powershell
python -m pytest -v -o addopts=""
```

The project has achieved 49 passing tests and 84% overall test coverage at the time this manual was prepared.

### 15. Conclusion

The Food Plant Operations Management System provides a centralized backend for managing important food manufacturing activities. It supports production tracking, material management, quality testing, approvals, historical data imports, reporting, authentication, and audit logging.
