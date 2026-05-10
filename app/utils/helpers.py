from app.core.logger import log

class Helpers:
    def check_task_type(task_type: str):
        VALID_TASK_TYPES = {"email", "image", "doc"}
        log.info(message="create_task",data={task_type: task_type}, fileName="task_service.py")
        if task_type not in VALID_TASK_TYPES:
            return False
        else:
            return True

helper = Helpers()