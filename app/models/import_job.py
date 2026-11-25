
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base


class ImportJob(Base):
    __tablename__ = "import_jobs"

    import_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    filename = Column(String(255), nullable=False)
    status = Column(String(30), default="Pending")

    total_rows = Column(Integer, default=0)
    successful_rows = Column(Integer, default=0)
    rejected_rows = Column(Integer, default=0)

    created_at = Column(DateTime, server_default=func.now())
