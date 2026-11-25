
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class QualityTest(Base):
    __tablename__ = "quality_tests"

    test_id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("batches.batch_id"), nullable=False)

    test_date = Column(Date, nullable=False)
    recorded_at = Column(DateTime, server_default=func.now())

    test_name = Column(String(100), nullable=False)
    result = Column(String(30), nullable=False)
    remarks = Column(String(255))
