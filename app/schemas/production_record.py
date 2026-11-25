
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class ProductionRecordCreate(BaseModel):
    batch_id: int
    input_quantity: float = Field(gt=0)
    output_quantity: float = Field(ge=0)
    wastage_quantity: float = Field(ge=0)
    moisture_reading: float | None = None


class ProductionRecordResponse(BaseModel):
    record_id: int
    batch_id: int
    input_quantity: float
    output_quantity: float
    wastage_quantity: float
    moisture_reading: float | None
    recorded_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
