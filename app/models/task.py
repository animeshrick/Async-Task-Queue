from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class TaskPayload(BaseModel):
    task_type: str = Field(..., description="Type of task to enqueue")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Task-specific payload")


class TaskStatusResponse(BaseModel):
    task_id: str
    task_type: str
    status: str
    payload: Dict[str, Any]
    result: Optional[Any] = None
    created_at: datetime
    updated_at: datetime
