import json
import time

from app.utils.redis_client import redis_client
from app.core.logger import log
from app.services.task_service import _iso_timestamp, TASK_QUEUE_KEY, TASK_PREFIX

from app.workers.executor import execute_task

def start_worker():
    print("Worker started...")

    while True:
        try:
            # blocking pop (waits until task arrives)
            _, task_data = redis_client.blpop(TASK_QUEUE_KEY)

            task = json.loads(task_data)
            task_id = task["task_id"]

            log.info(message="Picked up task", data={"task_id": task_id}, fileName="worker.py")
            print("Picked up task")

            task_key = f"{TASK_PREFIX}{task_id}"

            # mark processing
            redis_client.hset(task_key, mapping={
                "status": "processing",
                "updated_at": _iso_timestamp()
            })

            try:
                result = execute_task(task)

                time.sleep(60)
                redis_client.hset(task_key, mapping={
                    "status": "success",
                    "result": json.dumps(result),
                    "updated_at": _iso_timestamp()
                })

                log.info(message="Task completed", data={"task_id": task_id}, fileName="worker.py")
                print("Task completed")

            except Exception as e:
                redis_client.hset(task_key, mapping={
                    "status": "failed",
                    "error": str(e),
                    "updated_at": _iso_timestamp()
                })

                log.error(message="Task failed", data={"task_id": task_id, "error": str(e)}, fileName="worker.py")

        except Exception as e:
            print(f"Worker loop error: {str(e)}")
            time.sleep(10)