
from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    product_name: str = Field(min_length=2, max_length=100)
    category: str
    description: str | None = None
    unit_price: float = Field(default=0.0, ge=0)


class ProductResponse(BaseModel):
    product_id: int
    product_name: str
    category: str
    description: str | None
    unit_price: float
    is_active: int

    model_config = ConfigDict(from_attributes=True)
