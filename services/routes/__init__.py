"""
ZAYVORA Health OS — Modular Domain Routing Package
===================================================
Provides decoupled, domain-specific request dispatchers for ZAYVORA live API services.
"""

from .agentic_routes import handle_agentic_get, handle_agentic_post
from .auth_routes import handle_auth_get, handle_auth_post
from .pharmacy_routes import handle_pharmacy_get, handle_pharmacy_post
from .clinical_routes import handle_clinical_get, handle_clinical_post

__all__ = [
    "handle_agentic_get",
    "handle_agentic_post",
    "handle_auth_get",
    "handle_auth_post",
    "handle_pharmacy_get",
    "handle_pharmacy_post",
    "handle_clinical_get",
    "handle_clinical_post",
]
