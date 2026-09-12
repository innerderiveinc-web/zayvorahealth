"""
ZAYVORA HEALTH™ — Disaster Recovery Router
Provides endpoints for automated snapshot creation, backup verification, and RTO/RPO PITR health certification.
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional
from ..dr.backup_engine import DisasterRecoveryEngine

router = APIRouter(prefix="/api/v1/dr", tags=["Disaster Recovery & PITR"])


@router.post("/verify-snapshot", summary="Create and test-restore database snapshot")
async def verify_snapshot(database_name: str = "zayvora_clinical"):
    snapshot = DisasterRecoveryEngine.create_and_verify_snapshot(database_name)
    return {
        "snapshot_id": snapshot.snapshot_id,
        "database_name": snapshot.database_name,
        "created_at_utc": snapshot.created_at_utc,
        "size_bytes": snapshot.size_bytes,
        "sha256_checksum": snapshot.sha256_checksum,
        "wal_sequence_start": snapshot.wal_sequence_start,
        "wal_sequence_end": snapshot.wal_sequence_end,
        "status": snapshot.status,
    }


@router.get("/pitr-health", summary="Verify Point-in-Time Recovery compliance (RTO < 1h, RPO < 5m)")
async def get_pitr_health():
    cert = DisasterRecoveryEngine.verify_pitr_health()
    return {
        "certificate_id": cert.certificate_id,
        "verified_at_utc": cert.verified_at_utc,
        "latest_snapshot_id": cert.latest_snapshot_id,
        "rto": {
            "target_seconds": cert.rto_target_seconds,
            "estimated_seconds": cert.rto_estimated_seconds,
            "status": cert.rto_status,
        },
        "rpo": {
            "target_seconds": cert.rpo_target_seconds,
            "actual_lag_seconds": cert.rpo_actual_lag_seconds,
            "status": cert.rpo_status,
        },
        "replication_health": cert.replication_health,
        "overall_dr_readiness": cert.overall_dr_readiness,
    }
