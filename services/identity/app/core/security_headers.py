"""
Security headers middleware for the ZAYVORA Identity service.

Adds the following HTTP response headers to every outgoing response in
accordance with OWASP recommendations and modern browser hardening:

    X-Content-Type-Options       – prevents MIME-type sniffing
    X-Frame-Options              – blocks clickjacking via iframes
    X-XSS-Protection             – legacy XSS filter (belt-and-suspenders)
    Strict-Transport-Security    – enforces HTTPS on compliant browsers
    Content-Security-Policy      – restricts resource loading origins
    Referrer-Policy              – limits referrer information leakage
    Permissions-Policy           – disables unnecessary browser features
"""
from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Starlette middleware that injects security-related HTTP response headers.

    Usage (in app factory / main.py)::

        from app.core.security_headers import SecurityHeadersMiddleware
        app.add_middleware(SecurityHeadersMiddleware)

    All header values follow the strictest settings that are still compatible
    with the ZAYVORA SPA (React / Next.js served from the same origin).
    Override *csp_policy* at construction time when different origins are
    required (e.g. in the staging environment).

    Args:
        app: The ASGI application to wrap.
        hsts_max_age: Max-Age in seconds for HSTS.  Defaults to 1 year.
        csp_policy: Full Content-Security-Policy string.  When ``None`` a
            safe default is used.
    """

    _DEFAULT_CSP = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "font-src 'self'; "
        "connect-src 'self'; "
        "frame-ancestors 'none'; "
        "form-action 'self'; "
        "base-uri 'self'; "
        "object-src 'none';"
    )

    def __init__(
        self,
        app: ASGIApp,
        *,
        hsts_max_age: int = 31_536_000,  # 1 year
        csp_policy: str | None = None,
    ) -> None:
        super().__init__(app)
        self._hsts_max_age = hsts_max_age
        self._csp = csp_policy or self._DEFAULT_CSP

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Forward the request and inject security headers into the response."""
        response: Response = await call_next(request)

        # Prevent MIME-type confusion attacks
        response.headers["X-Content-Type-Options"] = "nosniff"

        # Block rendering inside <iframe> / <frame> / <object>
        response.headers["X-Frame-Options"] = "DENY"

        # Legacy XSS filter – still honoured by some older browsers
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # Force HTTPS for 1 year; include sub-domains; allow preloading
        response.headers["Strict-Transport-Security"] = (
            f"max-age={self._hsts_max_age}; includeSubDomains; preload"
        )

        # Granular resource-loading policy
        response.headers["Content-Security-Policy"] = self._csp

        # Never send the full referrer URL cross-origin
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Disable unused, potentially privacy-invasive browser features
        response.headers["Permissions-Policy"] = (
            "accelerometer=(), "
            "ambient-light-sensor=(), "
            "autoplay=(), "
            "battery=(), "
            "camera=(), "
            "cross-origin-isolated=(), "
            "display-capture=(), "
            "document-domain=(), "
            "encrypted-media=(), "
            "execution-while-not-rendered=(), "
            "execution-while-out-of-viewport=(), "
            "fullscreen=(), "
            "geolocation=(), "
            "gyroscope=(), "
            "keyboard-map=(), "
            "magnetometer=(), "
            "microphone=(), "
            "midi=(), "
            "navigation-override=(), "
            "payment=(), "
            "picture-in-picture=(), "
            "publickey-credentials-get=(), "
            "screen-wake-lock=(), "
            "sync-xhr=(), "
            "usb=(), "
            "web-share=(), "
            "xr-spatial-tracking=()"
        )

        return response
