from fastapi import APIRouter, Depends, HTTPException

from schemas.tasks import TaskIn, TaskResponse, TaskUpdate
from services.tasks import TaskService

router = APIRouter(tags=["tasks"])


@router.post("/tasks", status_code=201, response_model=TaskResponse)
def create_task(raw_task: TaskIn, service: TaskService = Depends()):
    task = service.create_task(raw_task)
    return TaskResponse(**task)


@router.get("/tasks", status_code=200, response_model=list[TaskResponse])
def get_tasks(service: TaskService = Depends()):
    return service.get_all_tasks()


@router.get("/tasks/{task_id}", status_code=200, response_model=TaskResponse)
def get_task(task_id: int, service: TaskService = Depends()):
    task = service.get_task_by_id(task_id)
    if task["success"]:
        return TaskResponse(**task)
    raise HTTPException(status_code=404, detail=task["message"])


@router.patch("/tasks/{task_id}", status_code=200, response_model=TaskResponse)
def update_task(task_id: int, upd_data: TaskUpdate, service: TaskService = Depends()):
    task = service.edit_task(task_id, upd_data)
    if task["success"]:
        return TaskResponse(**task)
    raise HTTPException(status_code=404, detail=task["message"])


@router.delete("/tasks/{task_id}", status_code=200)
def delete_task(task_id: int, service: TaskService = Depends()):
    delete_result = service.delete_task(task_id)
    if delete_result["success"]:
        return delete_result
    raise HTTPException(status_code=404, detail=delete_result["message"])
