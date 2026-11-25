
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.production_record import ProductionRecord
from app.schemas.production_record import (
    ProductionRecordCreate,
    ProductionRecordResponse
)
from app.routers.auth_router import require_roles
from app.models.user import User
from app.services.audit_service import create_audit_log
router = APIRouter(
    prefix="/production-records",
    tags=["Production Records"]
)

@router.post("/", response_model=ProductionRecordResponse)
def create_production_record(
    record: ProductionRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("Admin"))
):
    new_record = ProductionRecord(**record.model_dump())

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    create_audit_log(
        db=db,
        user_id=current_user.user_id,
        action="CREATE",
        entity_type="ProductionRecord",
        entity_id=new_record.record_id,
        details=(
            f"Production record created. "
            f"Record ID: {new_record.record_id}. "
            f"Batch ID: {new_record.batch_id}. "
            f"Input: {new_record.input_quantity}. "
            f"Output: {new_record.output_quantity}. "
            f"Wastage: {new_record.wastage_quantity}."
        )
    )

    return new_record



@router.get("/", response_model=list[ProductionRecordResponse])
def get_production_records(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("Admin"))
):
    return db.query(ProductionRecord).all()


@router.get("/{record_id}", response_model=ProductionRecordResponse)
def get_production_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("Admin"))
):
    record = db.query(ProductionRecord).filter(
        ProductionRecord.record_id == record_id
    ).first()

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Production record not found"
        )

    return record
