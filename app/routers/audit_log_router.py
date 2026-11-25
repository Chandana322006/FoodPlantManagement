
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.audit_log import AuditLog
from app.schemas.audit_log import (
    AuditLogCreate,
    AuditLogResponse
)
from app.routers.auth_router import require_roles
from app.models.user import User

router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"]
)


@router.post("/", response_model=AuditLogResponse)
def create_audit_log(
    log: AuditLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("Admin"))
):
    new_log = AuditLog(**log.model_dump())

    db.add(new_log)
    db.commit()
    db.refresh(new_log)

    return new_log


@router.get("/", response_model=list[AuditLogResponse])
def get_audit_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("Admin"))
):
    return db.query(AuditLog).order_by(
        AuditLog.timestamp.desc()
    ).all()
