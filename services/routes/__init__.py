"""
ZAYVORA Health OS — Modular Domain Routing Package
===================================================
Provides decoupled, domain-specific request dispatchers for ZAYVORA live API services.
"""

from .agentic_routes import handle_agentic_get, handle_agentic_post

__all__ = [
    "handle_agentic_get",
    "handle_agentic_post",
]
