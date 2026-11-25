
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.raw_material import RawMaterial
from app.schemas.raw_material import (
    RawMaterialCreate,
    RawMaterialResponse
)
from app.routers.auth_router import require_roles
from app.models.user import User

router = APIRouter(
    prefix="/raw-materials",
    tags=["Raw Materials"]
)


@router.post("/", response_model=RawMaterialResponse)
def create_raw_material(
    material: RawMaterialCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("Admin"))
):
    existing_material = db.query(RawMaterial).filter(
        RawMaterial.material_name == material.material_name
    ).first()

    if existing_material:
        raise HTTPException(
            status_code=400,
            detail="Raw material already exists"
        )

    new_material = RawMaterial(**material.model_dump())

    db.add(new_material)
    db.commit()
    db.refresh(new_material)

    return new_material


@router.get("/", response_model=list[RawMaterialResponse])
def get_raw_materials(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("Admin"))
):
    return db.query(RawMaterial).all()
