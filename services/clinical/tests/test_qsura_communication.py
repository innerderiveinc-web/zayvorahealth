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

from app.qsura.communication_broker import QSURACommunicationBroker


def test_qsura_appointment_confirmation():
    broker = QSURACommunicationBroker()
    res = broker.send_notification(
        channel="whatsapp",
        recipient="+919876543210",
        message_type="APPOINTMENT_CONFIRMATION",
        parameters={
            "patient_name": "Zayd Khan",
            "practitioner_name": "Hakim Irfan",
            "appointment_time": "2026-09-15 10:30 AM",
            "clinic_name": "ZAYVORA Health Central",
        },
    )
    assert res["delivery_status"] == "DELIVERED"
    assert "Hakim Irfan" in res["rendered_content"]
    assert "Zayd Khan" in res["rendered_content"]
    assert "MSG-" in res["message_id"]


def test_qsura_mudabbar_safety_advisory():
    broker = QSURACommunicationBroker()
    res = broker.send_notification(
        channel="whatsapp",
        recipient="+919876543210",
        message_type="MUDABBAR_SAFETY_ADVISORY",
        parameters={
            "patient_name": "Fatima",
            "medication_name": "Majun Suranjan",
            "dose": "5g twice daily with warm water",
            "helpline_number": "1800-ZAYVORA",
        },
    )
    assert res["delivery_status"] == "DELIVERED"
    assert "SAFETY ADVISORY" in res["rendered_content"]
    assert "Schedule E(1)" in res["rendered_content"]
    assert "1800-ZAYVORA" in res["rendered_content"]


def test_qsura_sms_phi_masking():
    broker = QSURACommunicationBroker()
    res = broker.send_notification(
        channel="sms",
        recipient="+919876543210",
        message_type="DISPENSE_READY_NOTIFICATION",
        parameters={
            "patient_name": "Ali",
            "batch_number": "BATCH-998877665544",
            "dosage_summary": "10ml syrup after meals",
        },
    )
    assert res["channel"] == "sms"
    # Long digit sequences should be masked
    assert "******" in res["rendered_content"]


def test_qsura_consent_enforcement():
    broker = QSURACommunicationBroker()
    with pytest.raises(PermissionError, match="DISHA/GDPR Consent Violation"):
        broker.send_notification(
            channel="whatsapp",
            recipient="+919876543210",
            message_type="APPOINTMENT_CONFIRMATION",
            parameters={
                "patient_name": "Zayd",
                "practitioner_name": "Hakim",
                "appointment_time": "Tomorrow",
                "clinic_name": "Clinic",
            },
            patient_consent_verified=False,
        )


def test_qsura_missing_required_params():
    broker = QSURACommunicationBroker()
    with pytest.raises(ValueError, match="Missing required template parameter"):
        broker.send_notification(
            channel="whatsapp",
            recipient="+919876543210",
            message_type="APPOINTMENT_CONFIRMATION",
            parameters={
                "patient_name": "Zayd",
                # Missing practitioner_name, appointment_time, clinic_name
            },
        )


def test_qsura_database_persistence_and_live_transport():
    class MockDbSession:
        def __init__(self):
            self.added = []
            self.committed = False

        def add(self, record):
            self.added.append(record)

        def commit(self):
            self.committed = True

    mock_db = MockDbSession()
    broker = QSURACommunicationBroker(db_session=mock_db)
    res = broker.send_notification(
        channel="whatsapp",
        recipient="+919876543210",
        message_type="APPOINTMENT_CONFIRMATION",
        parameters={
            "patient_name": "Sultana",
            "practitioner_name": "Dr. Tariq",
            "appointment_time": "2026-09-20 11:00 AM",
            "clinic_name": "ZAYVORA Apex",
        },
        organization_id="org-apex-01",
    )
    assert res["delivery_status"] in ("DELIVERED", "QUEUED_RETRY")
    assert len(mock_db.added) == 1
    assert mock_db.committed is True
    assert mock_db.added[0].recipient == "+919876543210"
    assert mock_db.added[0].organization_id == "org-apex-01"
