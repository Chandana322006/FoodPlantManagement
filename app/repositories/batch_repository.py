
from sqlalchemy.orm import Session

from app.models.batch import Batch


class BatchRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, batch: Batch):
        self.db.add(batch)
        self.db.commit()
        self.db.refresh(batch)
        return batch

    def get_by_id(self, batch_id: int):
        return (
            self.db.query(Batch)
            .filter(Batch.batch_id == batch_id)
            .first()
        )

    def get_all(self):
        return self.db.query(Batch).all()

    def update(self, batch: Batch):
        self.db.commit()
        self.db.refresh(batch)
        return batch

    def delete(self, batch: Batch):
        self.db.delete(batch)
        self.db.commit()
