
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class AuditLogCreate(BaseModel):
    user_id: int
    action: str
    entity_type: str
    entity_id: int
    details: str | None = None


class AuditLogResponse(BaseModel):
    log_id: int
    user_id: int
    action: str
    entity_type: str
    entity_id: int
    details: str | None
    timestamp: datetime | None

    model_config = ConfigDict(from_attributes=True)
