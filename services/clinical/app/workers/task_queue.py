"""
ZAYVORA Health™ — Asynchronous Task Queue & Background Worker Architecture.
Provides durable queueing with Redis backed storage and an in-memory thread-safe fallback.
"""
from __future__ import annotations

import json
import queue
import threading
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    RETRYING = "RETRYING"


class TaskType(str, Enum):
    ABDM_PACKET_RECONCILIATION = "abdm_packet_reconciliation"
    FHIR_BATCH_IMPORT = "fhir_batch_import"
    WEARABLE_STREAM_SYNC = "wearable_stream_sync"
    QSURA_DISPATCH = "qsura_dispatch"
    DIGITAL_TWIN_SIMULATION = "digital_twin_simulation"


@dataclass
class TaskRecord:
    task_id: str
    task_type: str
    organization_id: str
    payload: dict[str, Any]
    status: TaskStatus = TaskStatus.PENDING
    result: dict[str, Any] | None = None
    error: str | None = None
    safe_to_lock: bool = False
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    started_at: str | None = None
    completed_at: str | None = None
    retry_count: int = 0
    max_retries: int = 3

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        if isinstance(d["status"], TaskStatus):
            d["status"] = d["status"].value
        return d

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TaskRecord:
        data_copy = dict(data)
        if "status" in data_copy and isinstance(data_copy["status"], str):
            data_copy["status"] = TaskStatus(data_copy["status"])
        return cls(**data_copy)


class AsyncTaskQueue:
    """Thread-safe task broker supporting Redis and in-memory execution."""

    def __init__(self, redis_url: str | None = None):
        self._redis = None
        self._lock = threading.Lock()
        self._memory_queue: queue.Queue[str] = queue.Queue()
        self._dead_letter_queue: queue.Queue[str] = queue.Queue()
        self._dlq_tasks: dict[str, TaskRecord] = {}
        self._tasks: dict[str, TaskRecord] = {}

        if redis_url:
            try:
                import redis
                client = redis.from_url(redis_url, decode_responses=True)
                client.ping()
                self._redis = client
            except Exception:
                self._redis = None

    @property
    def is_redis_connected(self) -> bool:
        return self._redis is not None

    def enqueue(
        self,
        task_type: str,
        organization_id: str,
        payload: dict[str, Any],
        max_retries: int = 3,
        safe_to_lock: bool = False,
    ) -> TaskRecord:
        """Enqueues a new background task."""
        task_id = str(uuid.uuid4())
        record = TaskRecord(
            task_id=task_id,
            task_type=task_type,
            organization_id=organization_id,
            payload=payload,
            status=TaskStatus.PENDING,
            safe_to_lock=safe_to_lock,
            max_retries=max_retries,
        )

        if self._redis is not None:
            try:
                raw = json.dumps(record.to_dict())
                self._redis.set(f"zayvora:task:{task_id}", raw)
                self._redis.lpush("zayvora:task_queue", task_id)
                return record
            except Exception:
                pass  # Fall back to in-memory

        with self._lock:
            self._tasks[task_id] = record
            self._memory_queue.put(task_id)

        return record

    def dequeue(self, timeout_seconds: float = 0.1) -> TaskRecord | None:
        """Retrieves next pending task from queue."""
        if self._redis is not None:
            try:
                res = self._redis.brpop("zayvora:task_queue", timeout=int(max(1, timeout_seconds)))
                if res:
                    _, task_id = res
                    raw = self._redis.get(f"zayvora:task:{task_id}")
                    if raw:
                        record = TaskRecord.from_dict(json.loads(raw))
                        record.status = TaskStatus.PROCESSING
                        record.started_at = datetime.utcnow().isoformat()
                        self._redis.set(f"zayvora:task:{task_id}", json.dumps(record.to_dict()))
                        return record
            except Exception:
                pass  # Fall back to in-memory

        try:
            task_id = self._memory_queue.get(timeout=timeout_seconds)
            with self._lock:
                record = self._tasks.get(task_id)
                if record:
                    record.status = TaskStatus.PROCESSING
                    record.started_at = datetime.utcnow().isoformat()
                    return record
        except queue.Empty:
            return None

        return None

    def get_task(self, task_id: str) -> TaskRecord | None:
        """Fetches task record by ID."""
        if self._redis is not None:
            try:
                raw = self._redis.get(f"zayvora:task:{task_id}")
                if raw:
                    return TaskRecord.from_dict(json.loads(raw))
            except Exception:
                pass

        with self._lock:
            return self._tasks.get(task_id)

    def complete_task(
        self,
        task_id: str,
        result: dict[str, Any],
        safe_to_lock: bool = False,
    ) -> TaskRecord | None:
        """Marks a task as successfully completed."""
        record = self.get_task(task_id)
        if not record:
            return None

        record.status = TaskStatus.COMPLETED
        record.result = result
        record.error = None
        record.completed_at = datetime.utcnow().isoformat()
        record.safe_to_lock = safe_to_lock

        if self._redis is not None:
            try:
                self._redis.set(f"zayvora:task:{task_id}", json.dumps(record.to_dict()))
                return record
            except Exception:
                pass

        with self._lock:
            self._tasks[task_id] = record

        return record

    def fail_task(self, task_id: str, error: str) -> TaskRecord | None:
        """Handles task failure, triggering re-queueing if retries remain."""
        record = self.get_task(task_id)
        if not record:
            return None

        record.error = error
        record.retry_count += 1

        if record.retry_count <= record.max_retries:
            record.status = TaskStatus.RETRYING
            # Re-enqueue
            if self._redis is not None:
                try:
                    self._redis.set(f"zayvora:task:{task_id}", json.dumps(record.to_dict()))
                    self._redis.lpush("zayvora:task_queue", task_id)
                    return record
                except Exception:
                    pass
            with self._lock:
                self._tasks[task_id] = record
                self._memory_queue.put(task_id)
        else:
            record.status = TaskStatus.FAILED
            record.completed_at = datetime.utcnow().isoformat()
            if self._redis is not None:
                try:
                    self._redis.set(f"zayvora:task:{task_id}", json.dumps(record.to_dict()))
                    self._redis.lpush("zayvora:task_dlq", task_id)
                    return record
                except Exception:
                    pass
            with self._lock:
                self._tasks[task_id] = record
                self._dlq_tasks[task_id] = record
                self._dead_letter_queue.put(task_id)

        return record

    def list_dlq_tasks(
        self,
        organization_id: str | None = None,
        limit: int = 50,
    ) -> list[TaskRecord]:
        """Lists poison pill and terminally failed tasks preserved in DLQ."""
        results = []
        with self._lock:
            all_records = list(self._dlq_tasks.values())

        for r in all_records:
            if organization_id and r.organization_id != organization_id:
                continue
            results.append(r)
            if len(results) >= limit:
                break
        return results

    def requeue_dlq_task(self, task_id: str) -> TaskRecord | None:
        """Resets retry counter and re-enqueues a task from DLQ into active queue."""
        record = self.get_task(task_id)
        if not record or record.status != TaskStatus.FAILED:
            return None

        record.status = TaskStatus.PENDING
        record.retry_count = 0
        record.error = None
        record.completed_at = None

        if self._redis is not None:
            try:
                self._redis.set(f"zayvora:task:{task_id}", json.dumps(record.to_dict()))
                self._redis.lpush("zayvora:task_queue", task_id)
                self._redis.lrem("zayvora:task_dlq", 0, task_id)
                return record
            except Exception:
                pass

        with self._lock:
            self._tasks[task_id] = record
            if task_id in self._dlq_tasks:
                del self._dlq_tasks[task_id]
            self._memory_queue.put(task_id)

        return record

    def list_tasks(
        self,
        organization_id: str | None = None,
        status: TaskStatus | None = None,
        limit: int = 50,
    ) -> list[TaskRecord]:
        """Lists tasks matching filters."""
        results = []
        with self._lock:
            all_records = list(self._tasks.values())

        for r in all_records:
            if organization_id and r.organization_id != organization_id:
                continue
            if status and r.status != status:
                continue
            results.append(r)
            if len(results) >= limit:
                break

        # Sort descending by created_at
        results.sort(key=lambda x: x.created_at, reverse=True)
        return results

    def queue_size(self) -> int:
        """Returns approximate count of pending items."""
        if self._redis is not None:
            try:
                return int(self._redis.llen("zayvora:task_queue"))
            except Exception:
                pass
        return self._memory_queue.qsize()


# Singleton instance
GLOBAL_TASK_QUEUE = AsyncTaskQueue()
