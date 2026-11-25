
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.material_usage import MaterialUsage
from app.models.batch import Batch
from app.models.raw_material import RawMaterial
from app.schemas.material_usage import (
    MaterialUsageCreate,
    MaterialUsageResponse
)
from app.routers.auth_router import require_roles
from app.models.user import User
from app.services.audit_service import create_audit_log
router = APIRouter(
    prefix="/material-usage",
    tags=["Material Usage"]
)



@router.post("/", response_model=MaterialUsageResponse)
def create_material_usage(
    usage: MaterialUsageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("Admin"))
):
    batch = db.query(Batch).filter(
        Batch.batch_id == usage.batch_id
    ).first()

    material = db.query(RawMaterial).filter(
        RawMaterial.material_id == usage.material_id
    ).first()

    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")

    if not material:
        raise HTTPException(status_code=404, detail="Raw material not found")

    if material.quantity_available < usage.quantity_used:
        raise HTTPException(
            status_code=400,
            detail="Insufficient material quantity"
        )

    previous_quantity = material.quantity_available

    material.quantity_available -= usage.quantity_used

    new_usage = MaterialUsage(**usage.model_dump())

    db.add(new_usage)
    db.commit()
    db.refresh(new_usage)

    create_audit_log(
        db=db,
        user_id=current_user.user_id,
        action="CREATE",
        entity_type="MaterialUsage",
        entity_id=new_usage.usage_id,
        details=(
            f"Raw material used in production. "
            f"Batch ID: {new_usage.batch_id}. "
            f"Material ID: {new_usage.material_id}. "
            f"Quantity used: {new_usage.quantity_used}. "
            f"Previous stock: {previous_quantity}. "
            f"Remaining stock: {material.quantity_available}."
        )
    )

    return new_usage

   
     


@router.get("/", response_model=list[MaterialUsageResponse])
def get_material_usage(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("Admin"))
):
    return db.query(MaterialUsage).all()
