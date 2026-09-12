"""
ZAYVORA Health™ — Scheduled Cron Jobs Administration Router.
Enables triggering, monitoring, and inspecting periodic system jobs.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.auth_dependency import CurrentUser, require_permission
from app.workers.cron_scheduler import get_cron_scheduler

router = APIRouter(prefix="/api/v1/cron", tags=["scheduled-cron-jobs"])


@router.get("/status")
def get_cron_status_endpoint(
    user: CurrentUser = Depends(require_permission("system.admin")),
):
    """Returns status, schedule intervals, and execution metrics for all registered cron jobs."""
    scheduler = get_cron_scheduler()
    return scheduler.get_status()


@router.post("/trigger/{job_name}")
def trigger_cron_job_endpoint(
    job_name: str,
    user: CurrentUser = Depends(require_permission("system.admin")),
):
    """Manually triggers immediate execution of a registered cron job."""
    scheduler = get_cron_scheduler()
    try:
        result = scheduler.execute_job(job_name)
        return result
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cron job '{job_name}' not found. Check /api/v1/cron/status for registered jobs.",
        )
