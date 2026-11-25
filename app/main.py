
from fastapi import FastAPI
from app.database import engine, Base
from app import models
from app.routers import auth_router
from app.routers.role_router import router as role_router
from app.routers.product_router import router as product_router
from app.routers.production_line_router import router as production_line_router
from app.routers.supplier_router import router as supplier_router
from app.routers.batch_router import router as batch_router
from app.routers.raw_material_router import router as raw_material_router
from app.routers.production_record_router import router as production_record_router
from app.routers.quality_test_router import router as quality_test_router
from app.routers.approval_router import router as approval_router
from app.routers.audit_log_router import router as audit_log_router
from app.routers.machine_router import router as machine_router
from app.routers.material_usage_router import router as material_usage_router
from app.routers.user_router import router as user_router
from app.routers.import_router import router as import_router
from app.routers.report_router import router as report_router
from app.routers.export_router import router as export_router
from app.routers.auth_router import router as auth_router
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Food Plant Operations Management",
    description="Manage production, batches, suppliers and quality records.",
    version="1.0.0"
)

app.include_router(role_router)
app.include_router(product_router)
app.include_router(production_line_router)
app.include_router(supplier_router)
app.include_router(raw_material_router)
app.include_router(batch_router)
app.include_router(production_record_router)
app.include_router(quality_test_router)
app.include_router(approval_router)
app.include_router(audit_log_router)
app.include_router(machine_router)
app.include_router(material_usage_router)
app.include_router(user_router)
app.include_router(import_router)
app.include_router(report_router)
app.include_router(export_router)
app.include_router(user_router)
app.include_router(import_router)
app.include_router(report_router)
app.include_router(export_router)
app.include_router(auth_router)

@app.get("/")
def home():
    return {
        "message": "Welcome to Food Plant Operations Management App"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
