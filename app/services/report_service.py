
from sqlalchemy.orm import Session

from app.models.production_record import ProductionRecord
from app.models.quality_test import QualityTest

from app.strategies.production_strategy import (
    YieldStrategy,
    WastageStrategy
)


def get_production_report(db: Session):

    records = db.query(ProductionRecord).all()

    total_input = sum(record.input_quantity for record in records)
    total_output = sum(record.output_quantity for record in records)
    total_wastage = sum(record.wastage_quantity for record in records)

    yield_strategy = YieldStrategy()
    wastage_strategy = WastageStrategy()

    yield_percentage = yield_strategy.calculate(
        total_input, total_output, total_wastage
    )

    wastage_percentage = wastage_strategy.calculate(
        total_input, total_output, total_wastage
    )

    return {
        "total_input": round(total_input, 2),
        "total_output": round(total_output, 2),
        "total_wastage": round(total_wastage, 2),
        "yield_percentage": round(yield_percentage, 2),
        "wastage_percentage": round(wastage_percentage, 2)
    }


def get_quality_report(db: Session):

    tests = db.query(QualityTest).all()

    total_tests = len(tests)

    rejected_tests = sum(
        1 for test in tests
        if test.result.strip().lower() in ["rejected", "fail", "failed"]
    )

    if total_tests > 0:
        rejection_rate = (rejected_tests / total_tests) * 100
    else:
        rejection_rate = 0

    return {
        "total_tests": total_tests,
        "rejected_tests": rejected_tests,
        "rejection_rate": round(rejection_rate, 2)
    }
