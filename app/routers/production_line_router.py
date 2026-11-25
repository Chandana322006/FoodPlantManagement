
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.production_line import ProductionLine
from app.schemas.production_line import (
    ProductionLineCreate,
    ProductionLineResponse
)
from app.routers.auth_router import require_roles
from app.models.user import User

router = APIRouter(
    prefix="/production-lines",
    tags=["Production Lines"]
)


@router.post("/", response_model=ProductionLineResponse)
def create_production_line(
    line: ProductionLineCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("Admin"))
):
    existing_line = db.query(ProductionLine).filter(
        ProductionLine.line_name == line.line_name
    ).first()

    if existing_line:
        raise HTTPException(
            status_code=400,
            detail="Production line already exists"
        )

    new_line = ProductionLine(**line.model_dump())

    db.add(new_line)
    db.commit()
    db.refresh(new_line)

    return new_line


@router.get("/", response_model=list[ProductionLineResponse])
def get_production_lines(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("Admin"))
):
    return db.query(ProductionLine).all()
