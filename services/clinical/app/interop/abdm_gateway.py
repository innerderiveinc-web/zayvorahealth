"""
ZAYVORA ABDM (Ayushman Bharat Digital Mission) Gateway Client (Phase 12).

Simulates / interfaces with the NHA ABDM Gateway:
- ABHA Verification (Milestone 1)
- Consent Manager Handshake (Milestone 2)
- Health Data Exchange / FHIR Push (Milestone 3)
"""
from __future__ import annotations

import re
import uuid
from datetime import datetime, timedelta
from typing import Any


class ABDMGateway:
    def __init__(self, client_id: str = "zayvora-hip-hiu", gateway_url: str = "https://dev.abdm.gov.in/gateway"):
        self.client_id = client_id
        self.gateway_url = gateway_url
        self._consents: dict[str, dict[str, Any]] = {}

    def verify_abha(self, abha_id: str) -> dict[str, Any]:
        """Validates 14-digit ABHA number or @abdm / @sbx handle."""
        clean = abha_id.strip()

        # Check 14-digit format: e.g. 12-3456-7890-1234
        is_num = bool(re.match(r"^\d{2}-\d{4}-\d{4}-\d{4}$", clean))
        # Check ABHA address: e.g. name@abdm, name@sbx
        is_addr = bool(re.match(r"^[a-zA-Z0-9._-]+@(abdm|sbx|ndhm)$", clean))

        if not (is_num or is_addr):
            return {
                "valid": False,
                "error": "Invalid ABHA format. Expected 'XX-XXXX-XXXX-XXXX' or 'username@abdm'.",
                "abha_id": clean,
            }

        return {
            "valid": True,
            "abha_id": clean,
            "verification_status": "VERIFIED_ACTIVE",
            "linked_programs": ["AYUSH-Unani-Registry", "ABDM-PMJAY"],
            "verification_timestamp": datetime.utcnow().isoformat(),
        }

    def request_consent(
        self,
        *,
        patient_abha: str,
        hiu_id: str = "ZAYVORA-CLINIC-01",
        purpose_code: str = "CAREMGT",
        hi_types: list[str] | None = None,
        date_range_days: int = 180,
    ) -> dict[str, Any]:

        """Initiates an ABDM Consent Request to the patient's Ayushman Bharat Health Account."""
        hi_types = hi_types or ["OPConsultation", "Prescription", "DiagnosticReport"]
        consent_id = str(uuid.uuid4())

        now = datetime.utcnow()
        expiry = now + timedelta(days=30)
        from_date = now - timedelta(days=date_range_days)

        consent_record = {
            "consent_request_id": consent_id,
            "patient_abha": patient_abha,
            "status": "REQUESTED",
            "purpose": {
                "text": "Care Management and Unani Holistic Longitudinal Evaluation",
                "code": purpose_code,
            },
            "hi_types": hi_types,
            "permission": {
                "access_mode": "VIEW",
                "date_range": {
                    "from": from_date.isoformat(),
                    "to": now.isoformat(),
                },
                "data_erase_at": expiry.isoformat(),
                "frequency": {"unit": "HOUR", "value": 1, "repeats": 0},
            },
            "created_at": now.isoformat(),
            "last_updated": now.isoformat(),
        }

        self._consents[consent_id] = consent_record
        return consent_record

    def get_consent_status(self, consent_request_id: str) -> dict[str, Any] | None:
        """Checks status of an existing ABDM consent request."""
        return self._consents.get(consent_request_id)

    def grant_consent_mock(self, consent_request_id: str) -> dict[str, Any] | None:
        """Simulates patient approval of consent via ABHA mobile app."""
        record = self._consents.get(consent_request_id)
        if not record:
            return None
        record["status"] = "GRANTED"
        record["consent_artefact_id"] = str(uuid.uuid4())
        record["last_updated"] = datetime.utcnow().isoformat()
        return record
