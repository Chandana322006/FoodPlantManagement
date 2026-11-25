
from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.routers.auth_router import require_roles

from app.services.export_service import (
    export_report_csv,
    export_report_pdf
)

router = APIRouter(
    prefix="/exports",
    tags=["Report Exports"]
)


@router.get("/reports/csv")
def download_csv(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("Admin"))
):
    content = export_report_csv(db)

    return Response(
        content=content,
        media_type="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=food_plant_report.csv"
        }
    )


@router.get("/reports/pdf")
def download_pdf(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("Admin"))
):
    content = export_report_pdf(db)

    return Response(
        content=content,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
            "attachment; filename=food_plant_report.pdf"
        }
    )
