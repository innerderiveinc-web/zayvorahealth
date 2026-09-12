import contextlib

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

from app.engines.ebmr_engine import CANONICAL_MFRS, eBMRBatchSession


def test_ebmr_session_initialization():
    session = eBMRBatchSession(
        batch_number="FAL-2026-001",
        mfr_id="mfr-majun-falasifa",
        batch_size=10.0,
        operator_id="operator-1",
    )
    assert session.status == "STAGED"
    assert session.mfr["product_name"] == "Majun Falasifa"
    assert len(session.mfr["ingredients"]) == 7
    assert session.has_schedule_e1 is False


def test_ebmr_ipqc_pass():
    session = eBMRBatchSession(
        batch_number="FAL-2026-002",
        mfr_id="mfr-majun-falasifa",
        batch_size=10.0,
        operator_id="operator-1",
    )
    valid_assays = {
        "brix_refraction": 71.0,
        "ph_value": 5.2,
        "lead_pb_ppm": 0.8,
        "arsenic_as_ppm": 0.3,
        "total_bacterial_count": 50,
    }
    result = session.submit_ipqc_results(valid_assays)
    assert result["passed"] is True
    assert result["status"] == "PASSED"
    assert len(result["violations"]) == 0


def test_ebmr_ipqc_fail_heavy_metals():
    session = eBMRBatchSession(
        batch_number="FAL-2026-003",
        mfr_id="mfr-majun-falasifa",
        batch_size=10.0,
        operator_id="operator-1",
    )
    toxic_assays = {
        "brix_refraction": 71.0,
        "ph_value": 5.2,
        "lead_pb_ppm": 14.5,  # Exceeds max 10.0 ppm limit!
    }
    result = session.submit_ipqc_results(toxic_assays)
    assert result["passed"] is False
    assert result["status"] == "FAILED_SPECIFICATION"
    assert any("lead_pb_ppm" in v for v in result["violations"])


def test_ebmr_schedule_e1_mudabbar_gate_block():
    session = eBMRBatchSession(
        batch_number="SUR-2026-001",
        mfr_id="mfr-majun-suranjan",
        batch_size=10.0,
        operator_id="operator-suranjan",
    )
    assert session.has_schedule_e1 is True

    # Sign step 1
    session.record_stage_signoff(step_number=1, operator_id="op-1")

    # Attempt to release without step 2 (Mudabbar)
    session.submit_ipqc_results({
        "brix_refraction": 70.0,
        "ph_value": 5.0,
        "lead_pb_ppm": 1.0,
        "arsenic_as_ppm": 0.5,
        "total_bacterial_count": 100,
    })

    with pytest.raises(ValueError, match="QA RELEASE BLOCKED: Schedule E"):
        session.execute_final_qa_release(qa_director_id="qa-head-1")


def test_ebmr_successful_release_and_coa_generation():
    session = eBMRBatchSession(
        batch_number="SUR-2026-002",
        mfr_id="mfr-majun-suranjan",
        batch_size=10.0,
        operator_id="operator-suranjan",
    )

    # Sign all hold points
    session.record_stage_signoff(step_number=1, operator_id="op-1")
    # Step 2: Mudabbar step with verified certificate
    session.record_stage_signoff(
        step_number=2,
        operator_id="op-mudabbar-expert",
        mudabbar_cert_no="MUD-CERT-SUR-8841",
    )
    session.record_stage_signoff(step_number=4, operator_id="op-qa")

    # Submit valid IPQC assays
    session.submit_ipqc_results({
        "brix_refraction": 70.0,
        "ph_value": 5.0,
        "lead_pb_ppm": 0.9,
        "arsenic_as_ppm": 0.4,
        "total_bacterial_count": 80,
    })

    coa = session.execute_final_qa_release(qa_director_id="qa-director-01")
    assert session.status == "RELEASED"
    assert coa["verdict"] == "CERTIFIED_GMP_RELEASE"
    assert coa["mudabbar_certified"] is True
    assert coa["mudabbar_certificate_number"] == "MUD-CERT-SUR-8841"
    assert "COA-SUR-2026-002" in coa["certificate_id"]
