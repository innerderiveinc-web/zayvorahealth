"""
ZAYVORA Health OS — Modular Domain Routing Package
===================================================
Provides decoupled, domain-specific request dispatchers for ZAYVORA live API services.
"""

from .agentic_routes import handle_agentic_get, handle_agentic_post
from .auth_routes import handle_auth_get, handle_auth_post
from .pharmacy_routes import handle_pharmacy_get, handle_pharmacy_post
from .clinical_routes import handle_clinical_get, handle_clinical_post
from .computational_routes import handle_computational_get, handle_computational_post
from .telemedicine_routes import (
    handle_telemedicine_get,
    handle_telemedicine_post,
    handle_telemedicine_patch,
    handle_telemedicine_delete,
)
from .patient_routes import handle_patient_get, handle_patient_post
from .encounter_routes import handle_encounter_get, handle_encounter_post
from .billing_prescription_routes import (
    handle_billing_prescription_get,
    handle_billing_prescription_post,
)
from .diagnostics_operations_routes import (
    handle_operations_diagnostics_get,
    handle_operations_diagnostics_post,
)
from .continuum_trials_routes import (
    handle_continuum_trials_get,
    handle_continuum_trials_post,
)
from .governance_protocols_routes import (
    handle_governance_protocols_get,
    handle_governance_protocols_post,
)

__all__ = [
    "handle_agentic_get",
    "handle_agentic_post",
    "handle_auth_get",
    "handle_auth_post",
    "handle_pharmacy_get",
    "handle_pharmacy_post",
    "handle_clinical_get",
    "handle_clinical_post",
    "handle_computational_get",
    "handle_computational_post",
    "handle_telemedicine_get",
    "handle_telemedicine_post",
    "handle_telemedicine_patch",
    "handle_telemedicine_delete",
    "handle_patient_get",
    "handle_patient_post",
    "handle_encounter_get",
    "handle_encounter_post",
    "handle_billing_prescription_get",
    "handle_billing_prescription_post",
    "handle_operations_diagnostics_get",
    "handle_operations_diagnostics_post",
    "handle_continuum_trials_get",
    "handle_continuum_trials_post",
    "handle_governance_protocols_get",
    "handle_governance_protocols_post",
]
