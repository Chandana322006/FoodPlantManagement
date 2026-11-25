
from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base


class ProductionRecord(Base):
    __tablename__ = "production_records"

    record_id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("batches.batch_id"), nullable=False)

    input_quantity = Column(Float, nullable=False)
    output_quantity = Column(Float, nullable=False)
    wastage_quantity = Column(Float, nullable=False)

    moisture_reading = Column(Float, nullable=True)

    recorded_at = Column(DateTime, server_default=func.now())
