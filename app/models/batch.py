
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.database import Base


class Batch(Base):
    __tablename__ = "batches"

    batch_id = Column(Integer, primary_key=True, index=True)
    legacy_batch_number = Column(String(50), nullable=True)
    production_date = Column(Date, nullable=False)
    shift = Column(String(20), nullable=False)
    status = Column(String(30), default="Pending")

    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    line_id = Column(Integer, ForeignKey("production_lines.line_id"), nullable=False)
    created_by = Column(Integer, ForeignKey("users.user_id"), nullable=False)
