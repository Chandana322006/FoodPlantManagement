
import csv
import io
from datetime import date
from sqlalchemy.orm import Session
from app.models.batch import Batch
from app.models.production_record import ProductionRecord
from app.models.import_job import ImportJob
from app.models.import_issue import ImportIssue
from app.models.raw_material import RawMaterial
from app.models.supplier import Supplier
from app.models.machine import Machine
from app.models.production_line import ProductionLine
from app.models.quality_test import QualityTest
from app.models.product import Product
from app.models.user import User


def import_raw_materials_csv(file_content, filename, user_id, db: Session):

    job = ImportJob(
        user_id=user_id,
        filename=filename,
        status="Processing"
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    try:
        content = file_content.decode("utf-8-sig")

        content = "\n".join(
            line for line in content.splitlines()
            if line.strip()
        )

        reader = csv.DictReader(io.StringIO(content))

        required = {
            "material_name",
            "supplier_id",
            "unit",
            "quantity_available"
        }

        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            job.status = "Failed"
            db.commit()

            return {
                "import_id": job.import_id,
                "message": "CSV is missing required columns",
                "status": "Failed"
            }

        total = 0
        success = 0
        rejected = 0
        issues = []

        for row_number, row in enumerate(reader, start=2):
            total += 1

            try:
                name = row["material_name"].strip()
                supplier_id = int(row["supplier_id"])
                unit = row["unit"].strip()
                quantity = float(row["quantity_available"])

                if not name:
                    raise ValueError("Material name is required")

                if not unit:
                    raise ValueError("Unit is required")

                supplier = db.query(Supplier).filter(
                    Supplier.supplier_id == supplier_id
                ).first()

                if not supplier:
                    raise ValueError("Supplier does not exist")

                if quantity < 0:
                    raise ValueError("Quantity cannot be negative")

                db.add(RawMaterial(
                    material_name=name,
                    supplier_id=supplier_id,
                    unit=unit,
                    quantity_available=quantity
                ))

                success += 1

            except (ValueError, TypeError, KeyError) as error:

                rejected += 1

                db.add(ImportIssue(
                    import_id=job.import_id,
                    row_number=row_number,
                    reason=str(error),
                    raw_data=str(row)
                ))

                issues.append({
                    "row_number": row_number,
                    "reason": str(error),
                    "raw_data": str(row)
                })

        job.total_rows = total
        job.successful_rows = success
        job.rejected_rows = rejected

        job.status = (
            "Completed with errors"
            if rejected
            else "Completed"
        )

        db.commit()

        return {
            "import_id": job.import_id,
            "filename": filename,
            "total_rows": total,
            "successful_rows": success,
            "rejected_rows": rejected,
            "issues": issues,
            "status": job.status
        }

    except UnicodeDecodeError:

        job.status = "Failed"
        db.commit()

        return {
            "import_id": job.import_id,
            "filename": filename,
            "message": "Unable to read CSV. Use UTF-8 encoding.",
            "status": "Failed"
        }



        

def import_production_csv(file_content, filename, user_id, db: Session):
    job = ImportJob(
        user_id=user_id,
        filename=filename,
        status="Processing"
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    try:
        content = file_content.decode("utf-8-sig")
        reader = csv.DictReader(io.StringIO(content))

        required = {
            "batch_id", "input_quantity", "output_quantity",
            "wastage_quantity", "moisture_reading"
        }

        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            job.status = "Failed"
            db.commit()
            return {"import_id": job.import_id,
                    "message": "CSV is missing required columns",
                    "status": "Failed"}

        success = 0
        rejected = 0
        total = 0
        issues = []

        for row_number, row in enumerate(reader, start=2):
            total += 1
            try:
                batch_id = int(row["batch_id"])
                input_qty = float(row["input_quantity"])
                output_qty = float(row["output_quantity"])
                wastage = float(row["wastage_quantity"])

                moisture_text = row["moisture_reading"].strip()
                moisture = float(moisture_text) if moisture_text else None

                if not db.query(Batch).filter(
                    Batch.batch_id == batch_id
                ).first():
                    raise ValueError("Batch does not exist")

                if input_qty <= 0:
                    raise ValueError("Input quantity must be positive")

                if output_qty < 0 or wastage < 0:
                    raise ValueError("Output and wastage cannot be negative")

                if output_qty + wastage > input_qty:
                    raise ValueError(
                        "Output plus wastage cannot exceed input"
                    )

                if moisture is not None and not 0 <= moisture <= 100:
                    raise ValueError("Moisture must be between 0 and 100")

                db.add(ProductionRecord(
                    batch_id=batch_id,
                    input_quantity=input_qty,
                    output_quantity=output_qty,
                    wastage_quantity=wastage,
                    moisture_reading=moisture
                ))
                success += 1

            except (ValueError, TypeError, KeyError) as error:
                rejected += 1
                db.add(ImportIssue(
                    import_id=job.import_id,
                    row_number=row_number,
                    reason=str(error),
                    raw_data=str(row)
                ))
                issues.append({
                    "row_number": row_number,
                    "reason": str(error),
                    "raw_data": str(row)
                })

        job.total_rows = total
        job.successful_rows = success
        job.rejected_rows = rejected
        job.status = "Completed with errors" if rejected else "Completed"
        db.commit()

        return {
            "import_id": job.import_id,
            "filename": filename,
            "total_rows": total,
            "successful_rows": success,
            "rejected_rows": rejected,
            "issues": issues,
            "status": job.status
        }

    except UnicodeDecodeError:
        job.status = "Failed"
        db.commit()
        return {
            "import_id": job.import_id,
            "filename": filename,
            "message": "Unable to read CSV. Use UTF-8 encoding.",
            "status": "Failed"
        }



def import_machines_csv(file_content, filename, user_id, db: Session):

    job = ImportJob(
        user_id=user_id,
        filename=filename,
        status="Processing"
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    try:
        content = file_content.decode("utf-8-sig")

        content = "\n".join(
            line for line in content.splitlines()
            if line.strip()
        )

        reader = csv.DictReader(io.StringIO(content))

        required = {"machine_name", "machine_type", "line_id"}

        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            job.status = "Failed"
            db.commit()

            return {
                "import_id": job.import_id,
                "message": "CSV is missing required columns",
                "status": "Failed"
            }

        total = 0
        success = 0
        rejected = 0
        issues = []

        for row_number, row in enumerate(reader, start=2):
            total += 1

            try:
                name = row["machine_name"].strip()
                machine_type = row["machine_type"].strip()
                line_id = int(row["line_id"])

                if not name:
                    raise ValueError("Machine name is required")

                if not db.query(ProductionLine).filter(
                    ProductionLine.line_id == line_id
                ).first():
                    raise ValueError("Production line does not exist")

                db.add(Machine(
                    machine_name=name,
                    machine_type=machine_type,
                    line_id=line_id
                ))

                success += 1

            except (ValueError, TypeError, KeyError) as error:
                rejected += 1

                db.add(ImportIssue(
                    import_id=job.import_id,
                    row_number=row_number,
                    reason=str(error),
                    raw_data=str(row)
                ))

                issues.append({
                    "row_number": row_number,
                    "reason": str(error),
                    "raw_data": str(row)
                })

        job.total_rows = total
        job.successful_rows = success
        job.rejected_rows = rejected

        job.status = (
            "Completed with errors"
            if rejected
            else "Completed"
        )

        db.commit()

        return {
            "import_id": job.import_id,
            "filename": filename,
            "total_rows": total,
            "successful_rows": success,
            "rejected_rows": rejected,
            "issues": issues,
            "status": job.status
        }

    except UnicodeDecodeError:
        job.status = "Failed"
        db.commit()

        return {
            "import_id": job.import_id,
            "filename": filename,
            "message": "Unable to read CSV. Use UTF-8 encoding.",
            "status": "Failed"
        }

       
               
          

       



def import_quality_tests_csv(file_content, filename, user_id, db: Session):

    job = ImportJob(
        user_id=user_id,
        filename=filename,
        status="Processing"
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    try:
        content = file_content.decode("utf-8-sig")

        content = "\n".join(
            line for line in content.splitlines()
            if line.strip()
        )

        reader = csv.DictReader(io.StringIO(content))

        required = {
            "batch_id", "test_date", "test_name", "result", "remarks"
        }

        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            job.status = "Failed"
            db.commit()

            return {
                "import_id": job.import_id,
                "message": "CSV is missing required columns",
                "status": "Failed"
            }

        total = 0
        success = 0
        rejected = 0
        issues = []

        for row_number, row in enumerate(reader, start=2):
            total += 1

            try:
                batch_id = int(row["batch_id"])
                test_date = date.fromisoformat(row["test_date"].strip())
                test_name = row["test_name"].strip()
                result = row["result"].strip()
                remarks = row["remarks"].strip()

                if not test_name or not result:
                    raise ValueError("Test name and result are required")

                if not db.query(Batch).filter(
                    Batch.batch_id == batch_id
                ).first():
                    raise ValueError("Batch does not exist")

                db.add(QualityTest(
                    batch_id=batch_id,
                    test_date=test_date,
                    test_name=test_name,
                    result=result,
                    remarks=remarks
                ))

                success += 1

            except (ValueError, TypeError, KeyError) as error:
                rejected += 1

                db.add(ImportIssue(
                    import_id=job.import_id,
                    row_number=row_number,
                    reason=str(error),
                    raw_data=str(row)
                ))

                issues.append({
                    "row_number": row_number,
                    "reason": str(error),
                    "raw_data": str(row)
                })

        job.total_rows = total
        job.successful_rows = success
        job.rejected_rows = rejected

        job.status = (
            "Completed with errors"
            if rejected
            else "Completed"
        )

        db.commit()

        return {
            "import_id": job.import_id,
            "filename": filename,
            "total_rows": total,
            "successful_rows": success,
            "rejected_rows": rejected,
            "issues": issues,
            "status": job.status
        }

    except UnicodeDecodeError:
        job.status = "Failed"
        db.commit()

        return {
            "import_id": job.import_id,
            "filename": filename,
            "message": "Unable to read CSV. Use UTF-8 encoding.",
            "status": "Failed"
        }



def import_batches_csv(file_content, filename, user_id, db: Session):
    job = ImportJob(
        user_id=user_id,
        filename=filename,
        status="Processing"
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    try:
        content = file_content.decode("utf-8-sig")

# Remove blank csv.readerbefore reading the CSV
        content = "\n".join(
            line for line in content.splitlines()
            if line.strip()
        )

        reader = csv.DictReader(io.StringIO(content))

        if not reader.fieldnames:
            job.status = "Failed"
            db.commit()
            return {
                "import_id": job.import_id,
                "message": "CSV file is empty",
                "status": "Failed"
            }

        reader.fieldnames = [
            name.strip().lower() for name in reader.fieldnames
        ]

        required = {
            "legacy_batch_number", "production_date",
            "shift", "product_id", "line_id", "created_by"
        }

        if not required.issubset(reader.fieldnames):
            job.status = "Failed"
            db.commit()
            return {
                "import_id": job.import_id,
                "message": "CSV is missing required columns",
                "status": "Failed"
            }

        success = 0
        rejected = 0
        total = 0
        issues = []

        for row_number, row in enumerate(reader, start=2):
            total += 1
            try:
                legacy_number = (
                    row["legacy_batch_number"].strip() or None
                )
                production_date = date.fromisoformat(
                    row["production_date"].strip()
                )
                shift = row["shift"].strip()
                product_id = int(row["product_id"])
                line_id = int(row["line_id"])
                created_by = int(row["created_by"])

                if not shift:
                    raise ValueError("Shift is required")

                if not db.query(Product).filter(
                    Product.product_id == product_id
                ).first():
                    raise ValueError("Product does not exist")

                if not db.query(ProductionLine).filter(
                    ProductionLine.line_id == line_id
                ).first():
                    raise ValueError("Production line does not exist")

                if not db.query(User).filter(
                    User.user_id == created_by
                ).first():
                    raise ValueError("User does not exist")

                db.add(Batch(
                    legacy_batch_number=legacy_number,
                    production_date=production_date,
                    shift=shift,
                    status="Pending",
                    product_id=product_id,
                    line_id=line_id,
                    created_by=created_by
                ))
                success += 1

            except (ValueError, TypeError, KeyError) as error:
                rejected += 1

                db.add(ImportIssue(
                    import_id=job.import_id,
                    row_number=row_number,
                    reason=str(error),
                    raw_data=str(row)
                ))

                issues.append({
                    "row_number": row_number,
                    "reason": str(error),
                    "raw_data": str(row)
                })

        job.total_rows = total
        job.successful_rows = success
        job.rejected_rows = rejected
        job.status = "Completed with errors" if rejected else "Completed"

        db.commit()

        return {
            "import_id": job.import_id,
            "filename": filename,
            "total_rows": total,
            "successful_rows": success,
            "rejected_rows": rejected,
            "issues": issues,
            "status": job.status
        }

    except UnicodeDecodeError:
        job.status = "Failed"
        db.commit()
        return {
            "import_id": job.import_id,
            "filename": filename,
            "message": "Unable to read CSV. Use UTF-8 encoding.",
            "status": "Failed"
        }
