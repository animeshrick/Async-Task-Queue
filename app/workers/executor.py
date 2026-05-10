def execute_task(task: dict):
    task_type = task["task_type"]
    payload = task["payload"]

    if task_type == "email":
        return send_email(payload)

    elif task_type == "image":
        return upload_image(payload)
    
    elif task_type == "doc":
        return view_doc(payload)

    else:
        raise ValueError(f"Unknown task type: {task_type}")
    

def send_email(payload):
    return {"message": f"Email sent to {payload.get('to')}"}

def upload_image(payload):
    return {"message": f"Image: {payload}"}

def view_doc(payload):
    return {"message": f"Docs: {payload}"}