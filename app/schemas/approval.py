
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ApprovalCreate(BaseModel):
    batch_id: int
    reviewer_id: int
    comments: str | None = None


class ApprovalUpdate(BaseModel):
    status: str
    comments: str | None = None


class ApprovalResponse(BaseModel):
    approval_id: int
    batch_id: int
    reviewer_id: int
    status: str
    comments: str | None
    reviewed_at: datetime | None
    created_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
