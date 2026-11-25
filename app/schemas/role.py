
from pydantic import BaseModel, ConfigDict


class RoleCreate(BaseModel):
    role_name: str


class RoleResponse(BaseModel):
    role_id: int
    role_name: str

    model_config = ConfigDict(from_attributes=True)
