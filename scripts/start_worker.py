#!/usr/bin/env python
"""
Start the async task queue worker.
This script runs the worker process that processes tasks from the Redis queue.
"""

import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.workers.worker import start_worker


if __name__ == "__main__":
    print("Starting Async Task Queue Worker...")
    try:
        start_worker()
    except KeyboardInterrupt:
        print("\nWorker stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"Worker error: {e}")
        sys.exit(1)
