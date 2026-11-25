
from pydantic import BaseModel, ConfigDict, Field


class RawMaterialCreate(BaseModel):
    material_name: str
    supplier_id: int | None = None
    unit: str
    quantity_available: float = Field(default=0.0, ge=0)


class RawMaterialResponse(BaseModel):
    material_id: int
    material_name: str
    supplier_id: int | None
    unit: str
    quantity_available: float
    is_active: int

    model_config = ConfigDict(from_attributes=True)
