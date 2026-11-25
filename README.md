# Food Plant Operations Management System

A Python-based backend application built using FastAPI to manage food manufacturing operations, production records, raw materials, quality testing, approvals, and reporting.

## Project Overview

The Food Plant Operations Management System is designed to centralize the daily operations of a food manufacturing plant. It helps manage production activities, track material consumption, maintain quality records, handle historical CSV imports, and generate operational reports.

## Features

- **Authentication:** Login, bearer-token authentication, and role-based access control.
- **Master Data Management:** Products, suppliers, raw materials, production lines, machines, users, and roles.
- **Production Management:** Batch creation and production record tracking.
- **Material Management:** Material usage tracking and automatic stock deduction.
- **Quality Management:** Quality test recording and result tracking.
- **Approval Workflow:** Batch approval and status updates.
- **CSV Imports:** Import production, raw material, machine, quality test, and batch data.
- **Reports:** Production yield, wastage percentage, and quality rejection rate.
- **Report Exports:** CSV and PDF exports.
- **Audit Logging:** Records selected user activities and system operations.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | REST API development |
| SQLAlchemy | Database ORM |
| SQLite | Database |
| Pydantic | Data validation |
| Pytest | Automated testing |
| ReportLab | PDF report generation |

## Project Structure

```text
FoodPlantManagement/
│
├── app/
│   ├── models/
│   ├── schemas/
│   ├── routers/
│   ├── services/
│   ├── repositories/
│   ├── strategies/
│   ├── utils/
│   ├── database.py
│   └── main.py
│
├── tests/
├── imports/
├── reports/
├── diagrams/
├── docs/
│   └── user_manual.md
├── README.md
└── requirements.txt
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd FoodPlantManagement
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the Secret Key

Set a secure secret key before starting the application.

```powershell
$env:FOOD_PLANT_SECRET_KEY = (python -c "import secrets; print(secrets.token_urlsafe(48))")
```

### 6. Run the Application

```bash
uvicorn app.main:app --reload
```

### 7. Open API Documentation

Visit:

http://127.0.0.1:8000/docs

## Running Tests

Execute the test suite:

```bash
python -m pytest -v -o addopts=""
```

Generate test coverage:

```bash
python -m coverage run -m pytest -o addopts=""
python -m coverage report
python -m coverage html
```

**Current test results:** 49 passing tests and 84% overall test coverage.

## Design Patterns

The project uses:

1. **Repository Pattern:** Separates database operations from application logic.
2. **Strategy Pattern:** Implements production yield and wastage calculations using separate strategies.

## Documentation

Refer to `docs/user_manual.md` for instructions on using the application.

## Project Status

The backend includes authentication, production management, material tracking, quality testing, approvals, CSV imports, reporting, exports, and selected automatic audit logging.

Further improvements can include expanded role permissions, additional audit coverage, and a dedicated frontend.

## Author

Developed as a Python backend project using FastAPI.
