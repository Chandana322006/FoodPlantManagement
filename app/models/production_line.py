
from sqlalchemy import Column, Integer, String
from app.database import Base


class ProductionLine(Base):
    __tablename__ = "production_lines"

    line_id = Column(Integer, primary_key=True, index=True)
    line_name = Column(String(100), unique=True, nullable=False)
    location = Column(String(100))
    description = Column(String(255))
    is_active = Column(Integer, default=1)
