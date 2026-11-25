
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.approval import Approval
from app.models.batch import Batch
from app.models.user import User
from app.schemas.approval import (
    ApprovalCreate,
    ApprovalUpdate,
    ApprovalResponse
)
from app.routers.auth_router import require_roles
from app.services.audit_service import create_audit_log

router = APIRouter(
    prefix="/approvals",
    tags=["Approvals"]
)


@router.post("/", response_model=ApprovalResponse)
def create_approval(
    approval: ApprovalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("Admin"))
):
    batch = db.query(Batch).filter(
        Batch.batch_id == approval.batch_id
    ).first()

    if not batch:
        raise HTTPException(
            status_code=404,
            detail="Batch not found"
        )

    new_approval = Approval(
        batch_id=approval.batch_id,
        reviewer_id=approval.reviewer_id,
        status="Pending",
        comments=approval.comments
    )

    db.add(new_approval)
    db.commit()
    db.refresh(new_approval)

    return new_approval


@router.get("/", response_model=list[ApprovalResponse])
def get_approvals(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("Admin"))
):
    return db.query(Approval).all()


@router.put("/{approval_id}", response_model=ApprovalResponse)
def update_approval(
    approval_id: int,
    update: ApprovalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("Admin"))
):
    approval = db.query(Approval).filter(
        Approval.approval_id == approval_id
    ).first()

    if not approval:
        raise HTTPException(
            status_code=404,
            detail="Approval not found"
        )

    if update.status not in ["Approved", "Rejected"]:
        raise HTTPException(
            status_code=400,
            detail="Status must be Approved or Rejected"
        )

    previous_status = approval.status

    approval.status = update.status
    approval.comments = update.comments
    approval.reviewed_at = datetime.now()

    batch = db.query(Batch).filter(
        Batch.batch_id == approval.batch_id
    ).first()

    batch.status = update.status

    db.commit()
    db.refresh(approval)

    create_audit_log(
        db=db,
        user_id=current_user.user_id,
        action="UPDATE",
        entity_type="Approval",
        entity_id=approval.approval_id,
        details=(
            f"Approval status changed from "
            f"{previous_status} to {update.status}. "
            f"Batch ID: {approval.batch_id}. "
            f"Comments: {update.comments}"
        )
    )

    return approval
