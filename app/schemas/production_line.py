
from pydantic import BaseModel, ConfigDict


class ProductionLineCreate(BaseModel):
    line_name: str
    location: str | None = None
    description: str | None = None


class ProductionLineResponse(BaseModel):
    line_id: int
    line_name: str
    location: str | None
    description: str | None
    is_active: int

    model_config = ConfigDict(from_attributes=True)
