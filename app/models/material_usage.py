
from sqlalchemy import Column, Integer, Float, ForeignKey
from app.database import Base


class MaterialUsage(Base):
    __tablename__ = "material_usage"

    usage_id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("batches.batch_id"), nullable=False)
    material_id = Column(Integer, ForeignKey("raw_materials.material_id"), nullable=False)
    quantity_used = Column(Float, nullable=False)
