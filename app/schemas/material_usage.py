
from pydantic import BaseModel, ConfigDict, Field


class MaterialUsageCreate(BaseModel):
    batch_id: int
    material_id: int
    quantity_used: float = Field(gt=0)


class MaterialUsageResponse(BaseModel):
    usage_id: int
    batch_id: int
    material_id: int
    quantity_used: float

    model_config = ConfigDict(from_attributes=True)
