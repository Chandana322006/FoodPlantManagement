
from datetime import date

from app.services.import_service import import_production_csv
from app.models.role import Role
from app.models.user import User
from app.models.product import Product
from app.models.production_line import ProductionLine
from app.models.batch import Batch
from app.models.production_record import ProductionRecord
from app.models.import_issue import ImportIssue
from app.services.import_service import import_raw_materials_csv
from app.models.supplier import Supplier
from app.models.raw_material import RawMaterial
from app.services.import_service import import_machines_csv
from app.models.machine import Machine
from app.models.production_line import ProductionLine
from app.services.import_service import import_quality_tests_csv
from app.models.quality_test import QualityTest
from app.services.import_service import import_batches_csv
from app.models.batch import Batch

def create_test_batch(db_session):
    role = Role(role_name="Admin")
    db_session.add(role)
    db_session.commit()
    db_session.refresh(role)

    user = User(
        username="import_admin",
        email="import_admin@test.com",
        password_hash="test_hash",
        role_id=role.role_id
    )
    db_session.add(user)

    product = Product(
        product_name="Frozen Corn",
        category="Frozen Food",
        unit_price=100
    )

    line = ProductionLine(
        line_name="Import Test Line",
        location="Chennai"
    )

    db_session.add_all([product, line])
    db_session.commit()

    db_session.refresh(user)
    db_session.refresh(product)
    db_session.refresh(line)

    batch = Batch(
        production_date=date(2026, 1, 1),
        shift="Morning",
        product_id=product.product_id,
        line_id=line.line_id,
        created_by=user.user_id
    )

    db_session.add(batch)
    db_session.commit()
    db_session.refresh(batch)

    return batch, user


def test_production_import_with_valid_and_invalid_rows(db_session):
    batch, user = create_test_batch(db_session)

    csv_content = (
        "batch_id,input_quantity,output_quantity,"
        "wastage_quantity,moisture_reading\n"
        f"{batch.batch_id},100,90,10,\n"
        "999,100,80,20,12.5\n"
    ).encode("utf-8")

    result = import_production_csv(
        csv_content,
        "production_test.csv",
        user.user_id,
        db_session
    )

    assert result["total_rows"] == 2
    assert result["successful_rows"] == 1
    assert result["rejected_rows"] == 1
    assert result["status"] == "Completed with errors"

    record = db_session.query(ProductionRecord).first()

    assert record is not None
    assert record.moisture_reading is None

    issue = db_session.query(ImportIssue).first()

    assert issue is not None
    assert issue.row_number == 3
    assert issue.reason == "Batch does not exist"


def test_production_import_missing_columns(db_session):
    _, user = create_test_batch(db_session)

    csv_content = (
        "batch_id,input_quantity\n"
        "1,100\n"
    ).encode("utf-8")

    result = import_production_csv(
        csv_content,
        "invalid_columns.csv",
        user.user_id,
        db_session
    )

    assert result["status"] == "Failed"
    assert result["message"] == "CSV is missing required columns"

def create_test_supplier(db_session):
    supplier = Supplier(
        supplier_name="Test Supplier",
        contact_person="Test Contact",
        phone="9876543210",
        email="supplier@test.com",
        address="Chennai"
    )

    db_session.add(supplier)
    db_session.commit()
    db_session.refresh(supplier)

    return supplier


def test_raw_material_import_valid_and_invalid_rows(db_session):
    _, user = create_test_batch(db_session)
    supplier = create_test_supplier(db_session)

    csv_content = (
        "material_name,supplier_id,unit,quantity_available\n"
        f"Frozen Peas,{supplier.supplier_id},kg,100\n"
        "Frozen Corn,999,kg,50\n"
        f"Frozen Beans,{supplier.supplier_id},kg,-10\n"
    ).encode("utf-8")

    result = import_raw_materials_csv(
        csv_content,
        "raw_materials_test.csv",
        user.user_id,
        db_session
    )

    assert result["total_rows"] == 3
    assert result["successful_rows"] == 1
    assert result["rejected_rows"] == 2
    assert result["status"] == "Completed with errors"

    materials = db_session.query(RawMaterial).all()
    assert len(materials) == 1
    assert materials[0].material_name == "Frozen Peas"

    reasons = [issue["reason"] for issue in result["issues"]]

    assert "Supplier does not exist" in reasons
    assert "Quantity cannot be negative" in reasons


def test_raw_material_import_missing_columns(db_session):
    _, user = create_test_batch(db_session)

    csv_content = (
        "material_name,supplier_id\n"
        "Frozen Peas,1\n"
    ).encode("utf-8")

    result = import_raw_materials_csv(
        csv_content,
        "invalid_materials.csv",
        user.user_id,
        db_session
    )

    assert result["status"] == "Failed"
    assert result["message"] == "CSV is missing required columns"

def test_machine_import_valid_and_invalid_rows(db_session):
    _, user = create_test_batch(db_session)

    line = db_session.query(ProductionLine).filter(
        ProductionLine.line_name == "Import Test Line"
    ).first()

    csv_content = (
        "machine_name,machine_type,line_id\n"
        f"Freezer 1,Freezer,{line.line_id}\n"
        "Conveyor 1,Conveyor,999\n"
    ).encode("utf-8")

    result = import_machines_csv(
        csv_content,
        "machines_test.csv",
        user.user_id,
        db_session
    )

    assert result["total_rows"] == 2
    assert result["successful_rows"] == 1
    assert result["rejected_rows"] == 1
    assert result["status"] == "Completed with errors"

    machines = db_session.query(Machine).all()
    assert len(machines) == 1
    assert machines[0].machine_name == "Freezer 1"

    assert result["issues"][0]["reason"] == "Production line does not exist"


def test_machine_import_missing_columns(db_session):
    _, user = create_test_batch(db_session)

    csv_content = (
        "machine_name,machine_type\n"
        "Freezer 1,Freezer\n"
    ).encode("utf-8")

    result = import_machines_csv(
        csv_content,
        "invalid_machines.csv",
        user.user_id,
        db_session
    )

    assert result["status"] == "Failed"
    assert result["message"] == "CSV is missing required columns"

def test_quality_import_valid_and_invalid_rows(db_session):
    batch, user = create_test_batch(db_session)

    csv_content = (
        "batch_id,test_date,test_name,result,remarks\n"
        f"{batch.batch_id},2026-01-01,Moisture,Passed,Within limits\n"
        "999,2026-01-01,Texture,Rejected,Incorrect batch\n"
    ).encode("utf-8")

    result = import_quality_tests_csv(
        csv_content,
        "quality_tests.csv",
        user.user_id,
        db_session
    )

    assert result["total_rows"] == 2
    assert result["successful_rows"] == 1
    assert result["rejected_rows"] == 1
    assert result["status"] == "Completed with errors"

    quality_tests = db_session.query(QualityTest).all()
    assert len(quality_tests) == 1
    assert quality_tests[0].test_name == "Moisture"

    assert result["issues"][0]["reason"] == "Batch does not exist"


def test_quality_import_invalid_date(db_session):
    batch, user = create_test_batch(db_session)

    csv_content = (
        "batch_id,test_date,test_name,result,remarks\n"
        f"{batch.batch_id},invalid-date,Moisture,Passed,Test\n"
    ).encode("utf-8")

    result = import_quality_tests_csv(
        csv_content,
        "invalid_date.csv",
        user.user_id,
        db_session
    )

    assert result["total_rows"] == 1
    assert result["successful_rows"] == 0
    assert result["rejected_rows"] == 1
    assert result["status"] == "Completed with errors"

def test_batch_import_with_duplicate_legacy_numbers(db_session):
    batch, user = create_test_batch(db_session)

    csv_content = (
        "legacy_batch_number,production_date,shift,"
        "product_id,line_id,created_by\n"
        f"OLD-101,2026-01-02,Morning,"
        f"{batch.product_id},{batch.line_id},{user.user_id}\n"
        f"OLD-101,2026-01-03,Night,"
        f"{batch.product_id},{batch.line_id},{user.user_id}\n"
    ).encode("utf-8")

    result = import_batches_csv(
        csv_content,
        "batches_test.csv",
        user.user_id,
        db_session
    )

    assert result["total_rows"] == 2
    assert result["successful_rows"] == 2
    assert result["rejected_rows"] == 0
    assert result["status"] == "Completed"

    imported_batches = db_session.query(Batch).filter(
        Batch.legacy_batch_number == "OLD-101"
    ).all()

    assert len(imported_batches) == 2


def test_batch_import_invalid_product_and_line(db_session):
    _, user = create_test_batch(db_session)

    csv_content = (
        "legacy_batch_number,production_date,shift,"
        "product_id,line_id,created_by\n"
        f"OLD-102,2026-01-02,Morning,999,1,{user.user_id}\n"
        f"OLD-103,2026-01-03,Night,1,999,{user.user_id}\n"
    ).encode("utf-8")

    result = import_batches_csv(
        csv_content,
        "invalid_batches.csv",
        user.user_id,
        db_session
    )

    assert result["total_rows"] == 2
    assert result["successful_rows"] == 0
    assert result["rejected_rows"] == 2
    assert result["status"] == "Completed with errors"

    reasons = [issue["reason"] for issue in result["issues"]]

    assert "Product does not exist" in reasons
    assert "Production line does not exist" in reasons


def test_batch_import_missing_columns(db_session):
    _, user = create_test_batch(db_session)

    csv_content = (
        "legacy_batch_number,production_date,shift\n"
        "OLD-104,2026-01-02,Morning\n"
    ).encode("utf-8")

    result = import_batches_csv(
        csv_content,
        "missing_columns.csv",
        user.user_id,
        db_session
    )

    assert result["status"] == "Failed"
    assert result["message"] == "CSV is missing required columns"




