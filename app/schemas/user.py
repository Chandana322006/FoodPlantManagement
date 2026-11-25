
from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role_id: int


class UserResponse(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    role_id: int
    is_active: int

    model_config = ConfigDict(from_attributes=True)
