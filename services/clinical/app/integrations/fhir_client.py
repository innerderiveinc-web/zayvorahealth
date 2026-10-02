"""
FHIR R4 Client for ZAYVORA Clinical Service.

Supports SMART on FHIR OAuth2 authentication and standard FHIR R4 operations
for lab results (Observation resources) and conditions.
"""
from __future__ import annotations

import logging
import time
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


class FHIRAuthError(Exception):
    pass


class FHIRClientError(Exception):
    pass


class FHIRClient:
    """FHIR R4 client with SMART on FHIR OAuth2 support."""

    def __init__(
        self,
        base_url: str,
        client_id: str = "",
        client_secret: str = "",
        token_url: str = "",
        timeout: int = 30,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self.timeout = timeout
        self._access_token: str = ""
        self._token_expires_at: float = 0.0

        retry = Retry(total=3, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry)
        self._session = requests.Session()
        self._session.mount("https://", adapter)
        self._session.mount("http://", adapter)

    # ------------------------------------------------------------------
    # Auth
    # ------------------------------------------------------------------

    def authenticate(self) -> str:
        """Obtain (or refresh) an OAuth2 bearer token via client_credentials flow."""
        if not self.token_url or not self.client_id:
            return ""
        if self._access_token and time.time() < self._token_expires_at - 60:
            return self._access_token

        resp = self._session.post(
            self.token_url,
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "scope": "system/Observation.read system/Condition.read system/Observation.write",
            },
            timeout=self.timeout,
        )
        if not resp.ok:
            raise FHIRAuthError(f"FHIR auth failed: {resp.status_code} {resp.text}")

        data = resp.json()
        self._access_token = data["access_token"]
        self._token_expires_at = time.time() + data.get("expires_in", 3600)
        return self._access_token

    def _headers(self) -> dict[str, str]:
        token = self.authenticate()
        h = {"Accept": "application/fhir+json", "Content-Type": "application/fhir+json"}
        if token:
            h["Authorization"] = f"Bearer {token}"
        return h

    def _get(self, path: str, params: dict | None = None) -> dict:
        url = f"{self.base_url}/{path}"
        resp = self._session.get(url, headers=self._headers(), params=params, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def _post(self, path: str, body: dict) -> dict:
        url = f"{self.base_url}/{path}"
        resp = self._session.post(url, headers=self._headers(), json=body, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    # ------------------------------------------------------------------
    # Observations (Lab Results)
    # ------------------------------------------------------------------

    def get_observations(
        self,
        patient_id: str,
        category: str = "laboratory",
        date_from: str | None = None,
        date_to: str | None = None,
        count: int = 100,
    ) -> list[dict[str, Any]]:
        """Fetch FHIR Observation resources for a patient.

        Args:
            patient_id: FHIR Patient resource ID.
            category: Observation category (default: 'laboratory').
            date_from: ISO date string for range start (YYYY-MM-DD).
            date_to: ISO date string for range end (YYYY-MM-DD).
            count: Max results to return.

        Returns:
            List of FHIR Observation resource dicts.
        """
        params: dict[str, Any] = {
            "patient": patient_id,
            "category": category,
            "_count": count,
            "_sort": "-date",
        }
        if date_from:
            params["date"] = f"ge{date_from}"
        if date_to:
            params.setdefault("date", f"le{date_to}")

        try:
            bundle = self._get("Observation", params=params)
            entries = bundle.get("entry", [])
            return [e["resource"] for e in entries if "resource" in e]
        except Exception as exc:
            logger.error("FHIR get_observations failed: %s", exc)
            raise FHIRClientError(str(exc)) from exc

    def get_condition_list(self, patient_id: str) -> list[dict[str, Any]]:
        """Fetch active conditions for a patient."""
        try:
            bundle = self._get("Condition", params={"patient": patient_id, "clinical-status": "active"})
            return [e["resource"] for e in bundle.get("entry", []) if "resource" in e]
        except Exception as exc:
            logger.error("FHIR get_condition_list failed: %s", exc)
            raise FHIRClientError(str(exc)) from exc

    def create_observation(self, patient_id: str, data: dict[str, Any]) -> dict[str, Any]:
        """Post a new Observation resource to the FHIR server."""
        resource = {
            "resourceType": "Observation",
            "status": data.get("status", "final"),
            "category": [
                {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/observation-category",
                             "code": data.get("category", "laboratory")}]}
            ],
            "code": data.get("code", {}),
            "subject": {"reference": f"Patient/{patient_id}"},
            "effectiveDateTime": data.get("effectiveDateTime"),
            "valueQuantity": data.get("valueQuantity"),
        }
        try:
            return self._post("Observation", resource)
        except Exception as exc:
            logger.error("FHIR create_observation failed: %s", exc)
            raise FHIRClientError(str(exc)) from exc
