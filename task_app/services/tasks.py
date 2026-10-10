from fastapi import Depends

from repositories.tasks import TaskRepository
from schemas.tasks import TaskIn, TaskUpdate


class TaskService:
    def __init__(self, repository: TaskRepository = Depends()):
        self.repository = repository

    def create_task(self, task: TaskIn):
        db_task = self.repository.create(task)
        return {
            "success": True,
            "id": db_task.id,
            "title": db_task.title,
            "priority": db_task.priority,
        }

    def get_all_tasks(self):
        return self.repository.get_all()

    def get_task_by_id(self, task_id: int):
        task = self.repository.get_by_id(task_id)
        if task:
            return {
                "success": True,
                "id": task.id,
                "title": task.title,
                "priority": task.priority,
            }
        return {"success": False, "message": "Task not found."}

    def edit_task(self, task_id: int, upd_data: TaskUpdate):
        if not self.repository.get_by_id(task_id):
            return {"success": False, "message": "Task not found."}

        clear_dict = {k: v for k, v in upd_data.model_dump().items() if v is not None}
        task = self.repository.update(task_id, clear_dict)
        return {
            "success": True,
            "id": task.id,
            "title": task.title,
            "priority": task.priority,
        }

    def delete_task(self, task_id: int):
        if not self.repository.get_by_id(task_id):
            return {"success": False, "message": "Task not found."}

        self.repository.delete(task_id)
        return {"success": True, "message": "Task was deleted."}
