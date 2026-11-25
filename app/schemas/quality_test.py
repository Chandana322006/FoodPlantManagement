
from datetime import date, datetime
from pydantic import BaseModel, ConfigDict


class QualityTestCreate(BaseModel):
    batch_id: int
    test_date: date
    test_name: str
    result: str
    remarks: str | None = None


class QualityTestResponse(BaseModel):
    test_id: int
    batch_id: int
    test_date: date
    recorded_at: datetime | None
    test_name: str
    result: str
    remarks: str | None

    model_config = ConfigDict(from_attributes=True)
