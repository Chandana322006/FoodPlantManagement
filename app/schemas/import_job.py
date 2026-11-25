
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ImportJobCreate(BaseModel):
    user_id: int
    filename: str


class ImportJobResponse(BaseModel):
    import_id: int
    user_id: int
    filename: str
    status: str
    total_rows: int
    successful_rows: int
    rejected_rows: int
    created_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
