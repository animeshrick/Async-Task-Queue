Stack:
    FastAPI
    Redis
    Async workers

You implement:
    Task submission API
    Queue (Redis list / stream)
    Worker loop
    Retry logic
    Status tracking

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Project Structure
async-task-queue/
│
├── app/
│   ├── main.py                # FastAPI entrypoint
│   ├── core/
│   │   ├── config.py         # Settings (env, constants)
│   │   ├── logger.py         # Structured logging
│   │
│   ├── api/
│   │   ├── routes/
│   │   │   ├── tasks.py      # /submit-task, /status
│   │   │
│   │   └── deps.py           # Dependencies (Redis, etc.)
│   │
│   ├── models/
│   │   ├── task.py           # Pydantic models
│   │
│   ├── services/
│   │   ├── task_service.py   # Business logic (enqueue, status)
│   │
│   ├── workers/
│   │   ├── worker.py         # Worker loop
│   │   ├── executor.py       # Task execution logic
│   │
│   ├── utils/
│   │   ├── redis_client.py   # Redis connection
│   │   ├── helpers.py        # Common helpers
│
├── scripts/
│   ├── start_worker.py       # Run worker process
│
├── tests/
│   ├── test_tasks.py
│
├── .env
├── requirements.txt
├── README.md
└── docker-compose.yml

How this is designed (important)
    api/ → only HTTP layer
    services/ → logic (don’t mix with routes)
    workers/ → async background processing
    utils/ → shared infra (Redis, helpers)
    core/ → config + logging

👉 This separation is what makes your project look senior-level.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

POST /tasks
    - push task to queue

GET /tasks/{task_id}
    - Fetch from Redis
    - Return status + result


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Status Lifecycle
    pending → processing → success / failed

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Retry Strategy (this is where you level up)
    Basic version:
        If task fails:
        increment retry count
        requeue if retries < max_retries

Advanced:
    Add delay (backoff)
    Separate retry queue

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Client → FastAPI → Redis Queue → Worker → Redis Status → Client polls

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install dependencies:
    pip install -r requirements.txt

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Start the app:
    uvicorn app.main:app --reload
        http://127.0.0.1:8000
        http://127.0.0.1:8000/docs

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Start the worker:
    python scripts/start_worker.py

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a new task
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "task_type": "image",
    "payload": {
      "sound": "maww",
      "animal": "cat"
    }
  }'

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Get task status:
curl http://localhost:8000/tasks/{{task_id}}

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Email task:
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "task_type": "email",
    "payload": {
      "to": "user@example.com",
      "subject": "Test"
    }
  }'

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
