
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.routers.auth_router import require_roles

from app.services.report_service import (
    get_production_report,
    get_quality_report
)

router = APIRouter(
    prefix="/reports",
    tags=["Production Reports"]
)


@router.get("/production")
def production_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("Admin"))
):
    return get_production_report(db)


@router.get("/quality")
def quality_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("Admin"))
):
    return get_quality_report(db)
