import contextlib
from datetime import date

try:
    import pytest
except ImportError:
    class MockPytest:
        @staticmethod
        @contextlib.contextmanager
        def raises(expected_exception, match=None):
            try:
                yield
            except expected_exception as e:
                if match and match not in str(e):
                    raise AssertionError(f"Expected match '{match}' in '{str(e)}'")
            else:
                raise AssertionError(f"Expected {expected_exception} to be raised")

    pytest = MockPytest()

from app.engines.dispensary_engine import (
    ExpiredStockError,
    MudabbarDispenseBlockError,
    allocate_fefo_batches,
    execute_batch_recall,
)


def test_fefo_orders_by_earliest_expiry():
    batches = [
        {
            "id": "b-late",
            "batch_number": "BATCH-DEC",
            "expiry_date": "2026-12-31",
            "available_quantity": 200.0,
            "qc_release_status": "released",
        },
        {
            "id": "b-early",
            "batch_number": "BATCH-OCT",
            "expiry_date": "2026-10-15",
            "available_quantity": 100.0,
            "qc_release_status": "released",
        },
    ]

    res = allocate_fefo_batches(
        batches=batches,
        requested_quantity=150.0,
        current_date=date(2026, 9, 1),
    )

    assert res["status"] == "ALLOCATED"
    assert res["total_allocated"] == 150.0
    allocations = res["allocations"]
    assert len(allocations) == 2

    # Earliest batch (BATCH-OCT) allocated first!
    assert allocations[0]["batch_number"] == "BATCH-OCT"
    assert allocations[0]["allocated_quantity"] == 100.0

    # Remaining from BATCH-DEC
    assert allocations[1]["batch_number"] == "BATCH-DEC"
    assert allocations[1]["allocated_quantity"] == 50.0


def test_fefo_ignores_expired_and_quarantined():
    batches = [
        {
            "id": "b-expired",
            "batch_number": "BATCH-EXP",
            "expiry_date": "2026-01-01",  # Expired relative to 2026-09-01
            "available_quantity": 500.0,
            "qc_release_status": "released",
        },
        {
            "id": "b-quarantine",
            "batch_number": "BATCH-QC",
            "expiry_date": "2026-11-01",
            "available_quantity": 500.0,
            "qc_release_status": "quarantined",  # Not released
        },
        {
            "id": "b-valid",
            "batch_number": "BATCH-VALID",
            "expiry_date": "2026-10-01",
            "available_quantity": 50.0,
            "qc_release_status": "released",
        },
    ]

    res = allocate_fefo_batches(
        batches=batches,
        requested_quantity=100.0,
        current_date=date(2026, 9, 1),
    )

    # Only BATCH-VALID should be allocated
    assert res["total_allocated"] == 50.0
    assert res["status"] == "PARTIALLY_ALLOCATED"
    assert len(res["allocations"]) == 1
    assert res["allocations"][0]["batch_number"] == "BATCH-VALID"


def test_schedule_e1_mudabbar_gate_allows_certified():
    batches = [
        {
            "id": "b-suranjan-mudabbar",
            "batch_number": "SUR-MUD-001",
            "expiry_date": "2027-01-01",
            "available_quantity": 100.0,
            "qc_release_status": "released",
            "mudabbar_certified": True,
        }
    ]

    res = allocate_fefo_batches(
        batches=batches,
        requested_quantity=20.0,
        is_schedule_e1=True,
        current_date=date(2026, 9, 1),
    )

    assert res["status"] == "ALLOCATED"
    assert res["mudabbar_verified"] is True
    assert res["allocations"][0]["mudabbar_certified"] is True


def test_schedule_e1_mudabbar_gate_blocks_uncertified():
    batches = [
        {
            "id": "b-suranjan-kham",
            "batch_number": "SUR-RAW-001",
            "expiry_date": "2027-01-01",
            "available_quantity": 100.0,
            "qc_release_status": "released",
            "mudabbar_certified": False,  # Unpurified toxic batch!
        }
    ]

    with pytest.raises(MudabbarDispenseBlockError, match="DISPENSE GATE BLOCKED"):
        allocate_fefo_batches(
            batches=batches,
            requested_quantity=20.0,
            is_schedule_e1=True,
            current_date=date(2026, 9, 1),
        )


def test_execute_batch_recall_directive():
    batch = {
        "batch_number": "MAJUN-RECALL-99",
        "medication_name": "Majun Suranjan",
        "qc_release_status": "released",
    }

    directive = execute_batch_recall(
        batch=batch,
        reason="Stability assay failure: microbial overgrowth in warm storage lot.",
        recalled_by_user_id="pharmacist-admin-1",
        recall_class="CLASS_I",
    )

    assert directive["new_status"] == "recalled"
    assert directive["recall_class"] == "CLASS_I"
    assert "quarantine" in directive["action_required"].lower()
