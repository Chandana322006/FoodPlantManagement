
from pydantic import BaseModel, ConfigDict, EmailStr


class SupplierCreate(BaseModel):
    supplier_name: str
    contact_person: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    address: str | None = None


class SupplierResponse(BaseModel):
    supplier_id: int
    supplier_name: str
    contact_person: str | None
    phone: str | None
    email: str | None
    address: str | None
    is_active: int

    model_config = ConfigDict(from_attributes=True)
