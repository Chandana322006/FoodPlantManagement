
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.machine import Machine
from app.models.production_line import ProductionLine
from app.schemas.machine import MachineCreate, MachineResponse
from app.routers.auth_router import require_roles
from app.models.user import User

router = APIRouter(
    prefix="/machines",
    tags=["Machines"]
)


@router.post("/", response_model=MachineResponse)
def create_machine(
    machine: MachineCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("Admin"))
):
    line = db.query(ProductionLine).filter(
        ProductionLine.line_id == machine.line_id
    ).first()

    if not line:
        raise HTTPException(
            status_code=404,
            detail="Production line not found"
        )

    existing_machine = db.query(Machine).filter(
        Machine.machine_name == machine.machine_name,
        Machine.line_id == machine.line_id
    ).first()

    if existing_machine:
        raise HTTPException(
            status_code=400,
            detail="Machine already exists on this line"
        )

    new_machine = Machine(**machine.model_dump())

    db.add(new_machine)
    db.commit()
    db.refresh(new_machine)

    return new_machine


@router.get("/", response_model=list[MachineResponse])
def get_machines(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("Admin"))
):
    return db.query(Machine).all()
