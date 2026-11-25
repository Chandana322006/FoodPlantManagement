
from sqlalchemy import Column, Integer, String, Float
from app.database import Base


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(100), unique=True, nullable=False)
    category = Column(String(50), nullable=False)
    description = Column(String(255))
    unit_price = Column(Float, nullable=False, default=0.0)
    is_active = Column(Integer, default=1)
