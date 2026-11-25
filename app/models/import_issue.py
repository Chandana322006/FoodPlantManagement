
from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class ImportIssue(Base):
    __tablename__ = "import_issues"

    issue_id = Column(Integer, primary_key=True, index=True)
    import_id = Column(Integer, ForeignKey("import_jobs.import_id"), nullable=False)

    row_number = Column(Integer, nullable=False)
    reason = Column(String(500), nullable=False)
    raw_data = Column(String(1000))
