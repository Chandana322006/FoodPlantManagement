
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.batch import Batch
from app.schemas.batch import BatchCreate, BatchResponse
from app.repositories.batch_repository import BatchRepository
from app.routers.auth_router import require_roles
from app.models.user import User
from app.services.audit_service import create_audit_log
router = APIRouter(
    prefix="/batches",
    tags=["Batches"]
)


@router.post("/", response_model=BatchResponse)
def create_batch(
    batch: BatchCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("Admin"))
):
    new_batch = Batch(**batch.model_dump())

    repository = BatchRepository(db)
    created_batch = repository.create(new_batch)

    create_audit_log(
        db=db,
        user_id=current_user.user_id,
        action="CREATE",
        entity_type="Batch",
        entity_id=created_batch.batch_id,
        details=(
            f"New batch created. "
            f"Batch ID: {created_batch.batch_id}. "
            f"Product ID: {created_batch.product_id}. "
            f"Production Line ID: {created_batch.line_id}."
        )
    )

    return created_batch




@router.get("/", response_model=list[BatchResponse])
def get_batches(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("Admin"))
):
    repository = BatchRepository(db)
    return repository.get_all()


@router.get("/{batch_id}", response_model=BatchResponse)
def get_batch(
    batch_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("Admin"))
):
    repository = BatchRepository(db)

    batch = repository.get_by_id(batch_id)

    if not batch:
        raise HTTPException(
            status_code=404,
            detail="Batch not found"
        )

    return batch
