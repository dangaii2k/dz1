from fastapi import Depends
from sqlalchemy.orm import Session

from core.database import get_db
from models.tasks import Task
from schemas.tasks import TaskIn


class TaskRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create(self, task: TaskIn) -> Task:
        db_task = Task(**task.model_dump())
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def get_all(self) -> list[Task]:
        return self.db.query(Task).all()

    def get_by_id(self, task_id: int) -> Task | None:
        return self.db.query(Task).filter(Task.id == task_id).first()

    def update(self, task_id: int, upd_data: dict) -> Task | None:
        db_task = self.get_by_id(task_id)
        if not db_task:
            return None

        for key, value in upd_data.items():
            setattr(db_task, key, value)

        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def delete(self, task_id: int) -> bool:
        db_task = self.get_by_id(task_id)
        if not db_task:
            return False

        self.db.delete(db_task)
        self.db.commit()
        return True
