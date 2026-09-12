"""
ZAYVORA Pharmacy OS & FEFO Dispensing Engine (Phase 13).

Provides:
1. First-Expired, First-Out (FEFO) Inventory Allocation
2. Schedule E(1) Mandatory Mudabbar Verification at Dispense Gate
3. Automated Shelf-Life and Expiry Monitoring
4. Lot & Batch Safety Recall Protocol
"""
from __future__ import annotations

from datetime import date, datetime
from typing import Any


class MudabbarDispenseBlockError(ValueError):
    """Raised when a Schedule E(1) drug batch is attempted to be dispensed
    without authenticated Mudabbar detoxification certification."""
    pass


class ExpiredStockError(ValueError):
    """Raised when inventory has passed statutory shelf-life / expiry date."""
    pass


def parse_iso_date(d_str: str) -> date:
    return datetime.strptime(d_str.split("T")[0], "%Y-%m-%d").date()


def allocate_fefo_batches(
    *,
    batches: list[dict[str, Any]],
    requested_quantity: float,
    is_schedule_e1: bool = False,
    current_date: date | None = None,
) -> dict[str, Any]:
    """Allocates inventory batches strictly adhering to First-Expired, First-Out (FEFO)
    and Schedule E(1) statutory purification verification.
    """
    today = current_date or date.today()

    if requested_quantity <= 0:
        raise ValueError("Requested quantity must be greater than zero")

    eligible_batches: list[dict[str, Any]] = []

    for b in batches:
        # 1. Quality Control Gate
        if b.get("qc_release_status") != "released":
            continue

        # 2. Expiry Gate
        exp_date = parse_iso_date(b["expiry_date"])
        if exp_date <= today:
            continue

        # 3. Schedule E(1) Gate
        if is_schedule_e1:
            if not b.get("mudabbar_certified"):
                # Non-Mudabbar toxic batch cannot be allocated
                continue

        # 4. Stock Availability
        avail = float(b.get("available_quantity", 0.0))
        if avail <= 0.0:
            continue

        eligible_batches.append({**b, "_parsed_expiry": exp_date})

    # Sort strictly by Expiry Date ascending (FEFO)
    eligible_batches.sort(key=lambda x: x["_parsed_expiry"])

    if is_schedule_e1 and not eligible_batches:
        # Check if batches existed but were rejected due to uncertified Mudabbar
        uncertified = [b for b in batches if not b.get("mudabbar_certified")]
        if uncertified:
            raise MudabbarDispenseBlockError(
                "DISPENSE GATE BLOCKED: Schedule E(1) substance batch lacks validated Mudabbar detoxification certificate."
            )

    # Greedily allocate
    allocations = []
    needed = requested_quantity

    for eb in eligible_batches:
        avail = float(eb["available_quantity"])
        take = min(avail, needed)
        allocations.append({
            "batch_id": eb["id"],
            "batch_number": eb["batch_number"],
            "allocated_quantity": round(take, 2),
            "expiry_date": eb["expiry_date"],
            "days_until_expiry": (eb["_parsed_expiry"] - today).days,
            "mudabbar_certified": eb.get("mudabbar_certified", False),
        })
        needed -= take
        if needed <= 0.001:
            break

    total_allocated = round(sum(a["allocated_quantity"] for a in allocations), 2)
    fulfilled = total_allocated >= (requested_quantity - 0.001)

    return {
        "status": "ALLOCATED" if fulfilled else "PARTIALLY_ALLOCATED",
        "requested_quantity": requested_quantity,
        "total_allocated": total_allocated,
        "remaining_unfilled": round(max(0.0, requested_quantity - total_allocated), 2),
        "is_schedule_e1": is_schedule_e1,
        "mudabbar_verified": is_schedule_e1 and (total_allocated > 0),
        "allocations": allocations,
        "fefo_compliant": True,
    }


def execute_batch_recall(
    *,
    batch: dict[str, Any],
    reason: str,
    recalled_by_user_id: str,
    recall_class: str = "CLASS_I",
) -> dict[str, Any]:
    """Generates an emergency batch quarantine and recall directive."""
    return {
        "batch_number": batch["batch_number"],
        "medication_name": batch["medication_name"],
        "previous_status": batch.get("qc_release_status", "released"),
        "new_status": "recalled",
        "recall_class": recall_class,  # CLASS_I (Critical safety/toxicity), CLASS_II (Quality defect), CLASS_III (Minor)
        "reason": reason,
        "recalled_by_user_id": recalled_by_user_id,
        "recalled_at": datetime.utcnow().isoformat(),
        "action_required": "Immediate quarantine of all remaining stock. Notify treating clinicians and patients who received this batch.",
    }
