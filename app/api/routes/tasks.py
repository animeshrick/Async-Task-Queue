from fastapi import APIRouter, HTTPException

from app.models.task import TaskPayload, TaskStatusResponse
from app.services.task_service import create_task, get_task_status

router = APIRouter(tags=["tasks"])

@router.post("/tasks", status_code=201)
def submit_task(task: TaskPayload):
    return create_task(task.task_type, task.payload)

@router.get("/tasks/{task_id}", status_code=200)
def read_task(task_id: str):
    return get_task_status(task_id)
