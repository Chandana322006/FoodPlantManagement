
from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class Machine(Base):
    __tablename__ = "machines"

    machine_id = Column(Integer, primary_key=True, index=True)
    machine_name = Column(String(100), nullable=False)
    machine_type = Column(String(100))
    line_id = Column(
        Integer,
        ForeignKey("production_lines.line_id"),
        nullable=False
    )
    is_active = Column(Integer, default=1)
