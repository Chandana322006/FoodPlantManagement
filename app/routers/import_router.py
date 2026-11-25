
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.user import User
from app.models.import_job import ImportJob
from app.models.import_issue import ImportIssue
from app.routers.auth_router import require_roles

from app.services.import_service import (
    import_production_csv,
    import_raw_materials_csv,
    import_machines_csv,
    import_quality_tests_csv,
    import_batches_csv
)

from app.services.audit_service import create_audit_log


router = APIRouter(
    prefix="/imports",
    tags=["CSV Imports"]
)


def validate_csv_file(file: UploadFile):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed"
        )


def validate_user(user_id: int, db: Session):
    user = db.query(User).filter(
        User.user_id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


def log_import_audit(result, current_user, db, import_type):

    create_audit_log(
        db=db,
        user_id=current_user.user_id,
        action="IMPORT",
        entity_type="ImportJob",
        entity_id=result["import_id"],
        details=(
            f"{import_type} CSV import. "
            f"Filename: {result.get('filename', 'Unknown')}. "
            f"Status: {result.get('status')}. "
            f"Total rows: {result.get('total_rows', 0)}. "
            f"Successful rows: {result.get('successful_rows', 0)}. "
            f"Rejected rows: {result.get('rejected_rows', 0)}."
        )
    )

    return result


# 1. Import Production Records
@router.post("/production")
async def import_production(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("Admin"))
):
    validate_csv_file(file)
    validate_user(user_id, db)

    content = await file.read()

    result = import_production_csv(
        file_content=content,
        filename=file.filename,
        user_id=user_id,
        db=db
    )

    return log_import_audit(
        result, current_user, db, "Production"
    )


# 2. Import Raw Materials
@router.post("/raw-materials")
async def import_raw_materials(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("Admin"))
):
    validate_csv_file(file)
    validate_user(user_id, db)

    content = await file.read()

    result = import_raw_materials_csv(
        file_content=content,
        filename=file.filename,
        user_id=user_id,
        db=db
    )

    return log_import_audit(
        result, current_user, db, "Raw Materials"
    )


# 3. Import Machines
@router.post("/machines")
async def import_machines(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("Admin"))
):
    validate_csv_file(file)
    validate_user(user_id, db)

    content = await file.read()

    result = import_machines_csv(
        file_content=content,
        filename=file.filename,
        user_id=user_id,
        db=db
    )

    return log_import_audit(
        result, current_user, db, "Machines"
    )


# 4. Import Quality Tests
@router.post("/quality-tests")
async def import_quality_tests(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("Admin"))
):
    validate_csv_file(file)
    validate_user(user_id, db)

    content = await file.read()

    result = import_quality_tests_csv(
        file_content=content,
        filename=file.filename,
        user_id=user_id,
        db=db
    )

    return log_import_audit(
        result, current_user, db, "Quality Tests"
    )


# 5. Import Batches
@router.post("/batches")
async def import_batches(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("Admin"))
):
    validate_csv_file(file)
    validate_user(user_id, db)

    content = await file.read()

    result = import_batches_csv(
        file_content=content,
        filename=file.filename,
        user_id=user_id,
        db=db
    )

    return log_import_audit(
        result, current_user, db, "Batches"
    )


# 6. View All Import Jobs
@router.get("/jobs")
def get_import_jobs(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("Admin"))
):
    return db.query(ImportJob).order_by(
        ImportJob.import_id.desc()
    ).all()


# 7. View Import Validation Issues
@router.get("/{import_id}/issues")
def get_import_issues(
    import_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("Admin"))
):
    job = db.query(ImportJob).filter(
        ImportJob.import_id == import_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Import job not found"
        )

    return db.query(ImportIssue).filter(
        ImportIssue.import_id == import_id
    ).all()
