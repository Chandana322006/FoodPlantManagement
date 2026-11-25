
from pydantic import BaseModel, ConfigDict


class ImportIssueCreate(BaseModel):
    import_id: int
    row_number: int
    reason: str
    raw_data: str | None = None


class ImportIssueResponse(BaseModel):
    issue_id: int
    import_id: int
    row_number: int
    reason: str
    raw_data: str | None

    model_config = ConfigDict(from_attributes=True)
