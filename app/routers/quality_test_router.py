
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.quality_test import QualityTest
from app.schemas.quality_test import (
    QualityTestCreate,
    QualityTestResponse
)
from app.routers.auth_router import require_roles
from app.models.user import User
from app.services.audit_service import create_audit_log
router = APIRouter(
    prefix="/quality-tests",
    tags=["Quality Tests"]
)


@router.post("/", response_model=QualityTestResponse)
def create_quality_test(
    test: QualityTestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("Admin"))
):
    new_test = QualityTest(**test.model_dump())

    db.add(new_test)
    db.commit()
    db.refresh(new_test)

    create_audit_log(
        db=db,
        user_id=current_user.user_id,
        action="CREATE",
        entity_type="QualityTest",
        entity_id=new_test.test_id,
        details=(
            f"Quality test created. "
            f"Test ID: {new_test.test_id}. "
            f"Batch ID: {new_test.batch_id}. "
            f"Test name: {new_test.test_name}. "
            f"Result: {new_test.result}. "
            f"Remarks: {new_test.remarks}."
        )
    )

    return new_test


    

@router.get("/", response_model=list[QualityTestResponse])
def get_quality_tests(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("Admin"))
):
    return db.query(QualityTest).all()


@router.get("/{test_id}", response_model=QualityTestResponse)
def get_quality_test(
    test_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("Admin"))
):
    test = db.query(QualityTest).filter(
        QualityTest.test_id == test_id
    ).first()

    if not test:
        raise HTTPException(
            status_code=404,
            detail="Quality test not found"
        )

    return test
