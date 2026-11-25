
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.role import Role
from app.models.user import User
from app.schemas.role import RoleCreate, RoleResponse
from app.routers.auth_router import require_roles

router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)


@router.post("/", response_model=RoleResponse)
def create_role(
    role: RoleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("Admin"))
):
    existing_role = db.query(Role).filter(
        Role.role_name == role.role_name
    ).first()

    if existing_role:
        raise HTTPException(
            status_code=400,
            detail="Role already exists"
        )

    new_role = Role(role_name=role.role_name)

    db.add(new_role)
    db.commit()
    db.refresh(new_role)

    return new_role


@router.get("/", response_model=list[RoleResponse])
def get_roles(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("Admin"))
):
    return db.query(Role).all()
