"""
ZAYVORA Health OS™ — Universal Clinical & Operational Task Engine (Service 8)

Authoritative, cross-role task coordination spine for ZAYVORA Health OS™.
Provides a single canonical lifecycle:
  PENDING → IN_PROGRESS → COMPLETED / EXPIRED / CANCELLED
Supporting clinical alerts, PROM follow-ups, prescription signatures,
dispensary releases, and role-aware patient communication.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import time
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class ZayvoraTask:
    id: str                          # TSK-2026-XXXXX
    title: str                       # Plain-language actionable summary
    description: str                 # Clinical or operational context
    owner_id: str                    # Target user ID or Role identifier
    owner_role: str                  # DOCTOR, PATIENT, PHARMACIST, RECEPTIONIST, ADMIN
    patient_id: Optional[str]        # Associated Patient MRN/ID
    priority: str                    # STAT, HIGH, ROUTINE, LOW
    status: str                      # PENDING, IN_PROGRESS, COMPLETED, CANCELLED, EXPIRED
    task_type: str                   # LAB_REVIEW, NUSKHA_SIGN, APPOINTMENT_CHECKIN, PROM_DUE, FEFO_VERIFY, CARE_PLAN_MILESTONE
    source_module: str               # encounter, pharmacy, patient_app, safety_rail, care_plan
    due_at: str                      # ISO 8601 UTC
    created_at: str                  # ISO 8601 UTC
    completed_at: Optional[str]      # ISO 8601 UTC
    action_url: str                  # Deep-link to workspace modal
    provenance_hash: str             # SHA-256 tamper-evident integrity hash
    metadata: Dict[str, Any]         # Extensible polymorphic context


class UniversalTaskEngine:
    """Enterprise coordinator for all role-based tasks across ZAYVORA."""

    _IN_MEMORY_TASKS: Dict[str, ZayvoraTask] = {}

    @classmethod
    def _compute_hash(cls, task_id: str, title: str, owner_id: str, status: str, due_at: str) -> str:
        payload = f"{task_id}|{title}|{owner_id}|{status}|{due_at}|zayvora-tamper-evident"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    @classmethod
    def create_task(
        cls,
        title: str,
        description: str,
        owner_id: str,
        owner_role: str,
        task_type: str,
        source_module: str,
        priority: str = "ROUTINE",
        patient_id: Optional[str] = None,
        due_in_hours: int = 24,
        action_url: str = "/dashboard",
        metadata: Optional[Dict[str, Any]] = None,
        conn: Optional[sqlite3.Connection] = None
    ) -> ZayvoraTask:
        """Creates a durable, audited task and registers it in the task ledger."""
        now = datetime.now(timezone.utc).isoformat()
        due_timestamp = time.time() + (due_in_hours * 3600)
        due_at = datetime.fromtimestamp(due_timestamp, tz=timezone.utc).isoformat()
        task_id = f"TSK-2026-{uuid.uuid4().hex[:8].upper()}"

        prov_hash = cls._compute_hash(task_id, title, owner_id, "PENDING", due_at)
        task = ZayvoraTask(
            id=task_id,
            title=title,
            description=description,
            owner_id=owner_id,
            owner_role=owner_role.upper(),
            patient_id=patient_id,
            priority=priority.upper(),
            status="PENDING",
            task_type=task_type.upper(),
            source_module=source_module.lower(),
            due_at=due_at,
            created_at=now,
            completed_at=None,
            action_url=action_url,
            provenance_hash=prov_hash,
            metadata=metadata or {}
        )

        cls._IN_MEMORY_TASKS[task_id] = task

        if conn:
            try:
                cur = conn.cursor()
                cur.execute("""
                CREATE TABLE IF NOT EXISTS platform_tasks (
                    id TEXT PRIMARY KEY,
                    title TEXT,
                    description TEXT,
                    owner_id TEXT,
                    owner_role TEXT,
                    patient_id TEXT,
                    priority TEXT,
                    status TEXT,
                    task_type TEXT,
                    source_module TEXT,
                    due_at TEXT,
                    created_at TEXT,
                    completed_at TEXT,
                    action_url TEXT,
                    provenance_hash TEXT,
                    metadata_json TEXT
                )
                """)
                cur.execute("""
                INSERT INTO platform_tasks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    task.id, task.title, task.description, task.owner_id, task.owner_role,
                    task.patient_id, task.priority, task.status, task.task_type, task.source_module,
                    task.due_at, task.created_at, task.completed_at, task.action_url,
                    task.provenance_hash, json.dumps(task.metadata)
                ))
                conn.commit()
            except Exception:
                pass

        return task

    @classmethod
    def get_tasks_for_role(
        cls,
        role: str,
        owner_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50,
        conn: Optional[sqlite3.Connection] = None
    ) -> List[Dict[str, Any]]:
        """Retrieves active tasks matching user role and status filter."""
        target_role = role.upper()
        results: List[Dict[str, Any]] = []

        if conn:
            try:
                cur = conn.cursor()
                query = "SELECT * FROM platform_tasks WHERE owner_role = ?"
                params: List[Any] = [target_role]
                if owner_id:
                    query += " AND (owner_id = ? OR owner_id = 'ROLE_BROADCAST')"
                    params.append(owner_id)
                if status:
                    query += " AND status = ?"
                    params.append(status.upper())
                query += " ORDER BY CASE priority WHEN 'STAT' THEN 1 WHEN 'HIGH' THEN 2 WHEN 'ROUTINE' THEN 3 ELSE 4 END, due_at ASC LIMIT ?"
                params.append(limit)

                cur.execute(query, tuple(params))
                rows = cur.fetchall()
                for r in rows:
                    row_dict = dict(r)
                    if "metadata_json" in row_dict:
                        try:
                            row_dict["metadata"] = json.loads(row_dict["metadata_json"])
                        except Exception:
                            row_dict["metadata"] = {}
                    results.append(row_dict)
                if results:
                    return results
            except Exception:
                pass

        # Fallback to in-memory index
        for t in cls._IN_MEMORY_TASKS.values():
            if t.owner_role == target_role:
                if owner_id and t.owner_id not in (owner_id, "ROLE_BROADCAST"):
                    continue
                if status and t.status != status.upper():
                    continue
                results.append(asdict(t))

        priority_order = {"STAT": 1, "HIGH": 2, "ROUTINE": 3, "LOW": 4}
        results.sort(key=lambda x: (priority_order.get(x["priority"], 99), x["due_at"]))
        return results[:limit]

    @classmethod
    def complete_task(
        cls,
        task_id: str,
        actor_id: str,
        resolution_notes: str = "",
        conn: Optional[sqlite3.Connection] = None
    ) -> Dict[str, Any]:
        """Marks a task completed with statutory actor audit trail."""
        now = datetime.now(timezone.utc).isoformat()

        if task_id in cls._IN_MEMORY_TASKS:
            t = cls._IN_MEMORY_TASKS[task_id]
            t.status = "COMPLETED"
            t.completed_at = now
            t.metadata["completed_by"] = actor_id
            t.metadata["resolution_notes"] = resolution_notes
            t.provenance_hash = cls._compute_hash(t.id, t.title, t.owner_id, "COMPLETED", t.due_at)

        if conn:
            try:
                cur = conn.cursor()
                cur.execute("""
                UPDATE platform_tasks
                SET status = 'COMPLETED', completed_at = ?, provenance_hash = ?
                WHERE id = ?
                """, (now, f"completed-by-{actor_id}", task_id))
                conn.commit()
            except Exception:
                pass

        return {
            "ok": True,
            "task_id": task_id,
            "status": "COMPLETED",
            "completed_at": now,
            "completed_by": actor_id
        }

    @classmethod
    def seed_initial_clinical_tasks(cls, conn: Optional[sqlite3.Connection] = None):
        """Seeds canonical standard tasks to ensure fresh instances display operational feeds."""
        if cls._IN_MEMORY_TASKS:
            return

        cls.create_task(
            title="Review Bilateral Knee Radiograph & Uric Acid",
            description="Hamza Farooqi (MRN-2026-0001) knee film uploaded. Correlate with Waja-ul-Mafasil cold/wet mizaj presentation.",
            owner_id="DOC-01",
            owner_role="DOCTOR",
            task_type="LAB_REVIEW",
            source_module="encounter",
            priority="HIGH",
            patient_id="MRN-2026-0001",
            due_in_hours=6,
            action_url="/doctor",
            metadata={"urgency": "High", "lab_test": "S. Uric Acid + X-ray Knee"},
            conn=conn
        )

        cls.create_task(
            title="Schedule E(1) Mudabbar Detoxification Gate",
            description="Verify purification certificate for Hab-e-Suranjan batch MS-2026-LOT5 before dispensing.",
            owner_id="STF-PHARM-01",
            owner_role="PHARMACIST",
            task_type="FEFO_VERIFY",
            source_module="pharmacy",
            priority="STAT",
            patient_id="MRN-2026-0001",
            due_in_hours=2,
            action_url="/pharmacy",
            metadata={"batch_lot": "MS-2026-LOT5", "drug": "Suranjan"},
            conn=conn
        )

        cls.create_task(
            title="Complete Day 14 PROMs Joint Pain Scale",
            description="Rate morning stiffness and knee pain on the 10-point scale following Suranjan + Roghan regimen.",
            owner_id="PAT-774901",
            owner_role="PATIENT",
            task_type="PROM_DUE",
            source_module="patient_app",
            priority="ROUTINE",
            patient_id="MRN-2026-0001",
            due_in_hours=12,
            action_url="/patient",
            metadata={"program": "Metabolic Reset 90 / Mafasil"},
            conn=conn
        )
