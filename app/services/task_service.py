import json
import uuid
from datetime import datetime
from typing import Any, Dict

from app.models.task import TaskStatusResponse
from app.utils.redis_client import redis_client
from app.utils.helpers import Helpers

from app.core.logger import log

TASK_QUEUE_KEY = "/tasks/queue"
TASK_PREFIX = "/tasks/"
TASK_TTL_SECONDS = 60000 # 1min expiery time = 60

def _iso_timestamp() -> str:
    return datetime.utcnow().isoformat() + "Z"


def create_task(task_type: str, payload: Dict[str, Any]) -> TaskStatusResponse:
    try:
        task_id = str(uuid.uuid4())
        now = _iso_timestamp()
        task_key = f"{TASK_PREFIX}{task_id}"

        is_valid_task = Helpers.check_task_type(task_type)
        log.info(message="create_task",data={"valid_task": is_valid_task, task_type: task_type}, fileName="task_service.py")

        if is_valid_task == False:
            raise ValueError(f"Invalid task type: {task_type}")

        task_record = {
            "task_id": task_id,
            "task_type": task_type,
            "status": "pending",
            "payload": json.dumps(payload),
            "result": "",
            "created_at": now,
            "updated_at": now,
        }

        redis_client.hset(task_key, mapping=task_record)
        redis_client.expire(task_key, TASK_TTL_SECONDS)

        # Queue payload (store full task, not just ID)
        queue_payload = {
            "task_id": task_id,
            "task_type": task_type,
            "payload": payload,
        }
        redis_client.rpush(TASK_QUEUE_KEY, json.dumps(queue_payload))

        # Return response in the requested format
        return {
            "data": TaskStatusResponse(
                task_id=task_id,
                task_type=task_type,
                status="pending",
                payload=payload,
                result=None,
                created_at=now,
                updated_at=now,
            ),
            "message": "Success"
        }
    except Exception as ex:
        log.error(message="create_task_error",data={"error": ex}, fileName="task_service.py")
        return {
            "data": None,
            "message": "Failure"
        }


def get_task_status(task_id: str) -> TaskStatusResponse:
    try:
        debug = {}
        task_key = f"{TASK_PREFIX}{task_id}"
        if not redis_client.exists(task_key):
            raise KeyError("Task not found")

        data = redis_client.hgetall(task_key)
        payload = json.loads(data.get("payload", "{}")) if data.get("payload") else {}
        result_value = data.get("result")
        result: Any = None

        debug["task_key"] = task_key
        debug["data"] = data
        debug["payload"] = payload
        debug["result_value"] = result_value

        if result_value:
            try:
                result = json.loads(result_value)
            except json.JSONDecodeError:
                result = result_value

        debug["result"] = result

        log.info(message="debug_value", data=debug, fileName="task_service.py")

        # Parse ISO timestamps back to datetime objects
        created_at = datetime.fromisoformat(data["created_at"].replace("Z", "+00:00"))
        updated_at = datetime.fromisoformat(data["updated_at"].replace("Z", "+00:00"))

        return {
            "data": TaskStatusResponse(
                task_id=data["task_id"],
                task_type=data["task_type"],
                status=data["status"],
                payload=payload,
                result=result,
                created_at=created_at,
                updated_at=updated_at,
            ),
            "message": "Success"
        }
    except Exception as ex:
        log.error(message="get_task_status_error",data={"error": ex}, fileName="task_service.py")
        return {
            "data": None,
            "message": "Failure"
        }