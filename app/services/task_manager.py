import threading
import time
import uuid

_tasks: dict[str, dict] = {}
_lock = threading.Lock()

# Auto-cleanup after 30 minutes
_TTL = 1800


def create() -> str:
    task_id = uuid.uuid4().hex[:8]
    with _lock:
        _tasks[task_id] = {
            "status": "pending",
            "progress": {"current": 0, "total": 0},
            "result": None,
            "error": None,
            "created_at": time.time(),
        }
    return task_id


def update_progress(task_id: str, current: int, total: int):
    with _lock:
        t = _tasks.get(task_id)
        if t:
            t["status"] = "processing"
            t["progress"] = {"current": current, "total": total}


def set_done(task_id: str, result: dict):
    with _lock:
        t = _tasks.get(task_id)
        if t:
            t["status"] = "done"
            t["result"] = result


def set_error(task_id: str, error: str):
    with _lock:
        t = _tasks.get(task_id)
        if t:
            t["status"] = "error"
            t["error"] = error


def get(task_id: str) -> dict | None:
    with _lock:
        t = _tasks.get(task_id)
        if t is None:
            return None
        # Remove expired tasks
        if t["status"] == "done" and time.time() - t["created_at"] > _TTL:
            del _tasks[task_id]
            return None
        return {
            "task_id": task_id,
            "status": t["status"],
            "progress": t["progress"],
            "result": t["result"],
            "error": t["error"],
        }
