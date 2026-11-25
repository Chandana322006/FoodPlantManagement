
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base


class RawMaterial(Base):
    __tablename__ = "raw_materials"

    material_id = Column(Integer, primary_key=True, index=True)
    material_name = Column(String(100), nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.supplier_id"))
    unit = Column(String(30), nullable=False)
    quantity_available = Column(Float, default=0.0)
    is_active = Column(Integer, default=1)
