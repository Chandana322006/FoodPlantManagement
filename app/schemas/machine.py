
from pydantic import BaseModel, ConfigDict


class MachineCreate(BaseModel):
    machine_name: str
    machine_type: str | None = None
    line_id: int


class MachineResponse(BaseModel):
    machine_id: int
    machine_name: str
    machine_type: str | None
    line_id: int
    is_active: int

    model_config = ConfigDict(from_attributes=True)
