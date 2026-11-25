from datetime import date
from app.services.report_service import get_production_report, get_quality_report
from app.models.production_record import ProductionRecord
from app.models.quality_test import QualityTest

def test_production_report(db_session):

    records = [
        ProductionRecord(batch_id=1, input_quantity=100, output_quantity=90, wastage_quantity=10),
        ProductionRecord(batch_id=1, input_quantity=100, output_quantity=90, wastage_quantity=10),
        ProductionRecord(batch_id=1, input_quantity=200, output_quantity=180, wastage_quantity=20),
        ProductionRecord(batch_id=1, input_quantity=100, output_quantity=90, wastage_quantity=10),
        ProductionRecord(batch_id=1, input_quantity=200, output_quantity=180, wastage_quantity=20),
        ProductionRecord(batch_id=1, input_quantity=100, output_quantity=80, wastage_quantity=20)
    ]

    db_session.add_all(records)
    db_session.commit()

    report = get_production_report(db_session)

    assert report["total_input"] == 800
    assert report["total_output"] == 710
    assert report["total_wastage"] == 90
    assert report["yield_percentage"] == 88.75
    assert report["wastage_percentage"] == 11.25
def test_quality_report(db_session):

    tests = [
        QualityTest(batch_id=1, test_date=date(2026, 1, 1), test_name="Moisture", result="Passed"),
        QualityTest(batch_id=1, test_date=date(2026, 1, 1), test_name="Texture", result="Rejected"),
        QualityTest(batch_id=1, test_date=date(2026, 1, 1), test_name="Color", result="Passed"),
        QualityTest(batch_id=1, test_date=date(2026, 1, 1), test_name="Taste", result="Failed"),
    ]

    db_session.add_all(tests)
    db_session.commit()

    report = get_quality_report(db_session)

    assert report["total_tests"] == 4
    assert report["rejected_tests"] == 2
    assert report["rejection_rate"] == 50.0