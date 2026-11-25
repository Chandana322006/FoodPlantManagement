
from datetime import date
from pydantic import BaseModel, ConfigDict


class BatchCreate(BaseModel):
    legacy_batch_number: str | None = None
    production_date: date
    shift: str
    product_id: int
    line_id: int
    created_by: int


class BatchResponse(BaseModel):
    batch_id: int
    legacy_batch_number: str | None
    production_date: date
    shift: str
    status: str
    product_id: int
    line_id: int
    created_by: int

    model_config = ConfigDict(from_attributes=True)
