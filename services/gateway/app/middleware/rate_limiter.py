"""ZAYVORA HEALTH™ — Microservices Gateway Distributed Token-Bucket Rate Limiter
Enforces zero-trust request throttling:
- Unauthenticated requests: 60 requests / minute per client IP
- Authenticated requests: 600 requests / minute per client identity token
"""
from __future__ import annotations

import time
import threading
from typing import Optional, Tuple, Dict
try:
    from fastapi import Request, Response
    from starlette.middleware.base import BaseHTTPMiddleware
    from starlette.responses import JSONResponse
except ImportError:
    class Request: pass  # type: ignore
    class Response: pass  # type: ignore
    class BaseHTTPMiddleware:  # type: ignore
        def __init__(self, app): self.app = app
    class JSONResponse:  # type: ignore
        def __init__(self, status_code=200, content=None, headers=None):
            self.status_code = status_code
            self.content = content
            self.headers = headers or {}


class TokenBucketRateLimiter:
    """
    Token-bucket rate limiter with thread-safe in-memory cache and Redis compatibility.
    """

    def __init__(
        self,
        unauthenticated_limit: int = 60,
        authenticated_limit: int = 600,
        window_seconds: int = 60,
    ):
        self.unauthenticated_limit = unauthenticated_limit
        self.authenticated_limit = authenticated_limit
        self.window_seconds = window_seconds
        self._lock = threading.Lock()
        self._buckets: Dict[str, Tuple[float, float]] = {}

    def _get_client_key(self, request: Request) -> Tuple[str, bool, int]:
        auth_header = request.headers.get("Authorization") or request.headers.get("x-api-key")
        if auth_header and (auth_header.startswith("Bearer ") or auth_header.startswith("ak_")):
            key = f"auth:{auth_header[:32]}"
            return key, True, self.authenticated_limit

        forwarded_for = request.headers.get("x-forwarded-for")
        client_ip = forwarded_for.split(",")[0].strip() if forwarded_for else (request.client.host if request.client else "unknown")
        key = f"ip:{client_ip}"
        return key, False, self.unauthenticated_limit

    def check(self, request: Request) -> Tuple[bool, Dict[str, str]]:
        key, is_auth, max_limit = self._get_client_key(request)
        now = time.time()
        refill_rate = max_limit / self.window_seconds

        with self._lock:
            if key not in self._buckets:
                tokens = float(max_limit)
                last_time = now
            else:
                tokens, last_time = self._buckets[key]
                elapsed = now - last_time
                tokens = min(float(max_limit), tokens + elapsed * refill_rate)
                last_time = now

            headers = {
                "X-RateLimit-Limit": str(max_limit),
                "X-RateLimit-Remaining": str(max(0, int(tokens - 1))),
                "X-RateLimit-Reset": str(int(now + (max_limit - tokens) / refill_rate if refill_rate > 0 else now + self.window_seconds)),
            }

            if tokens >= 1.0:
                self._buckets[key] = (tokens - 1.0, last_time)
                return True, headers
            else:
                self._buckets[key] = (tokens, last_time)
                retry_after = int((1.0 - tokens) / refill_rate) + 1
                headers["Retry-After"] = str(retry_after)
                return False, headers


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limiter: Optional[TokenBucketRateLimiter] = None):
        super().__init__(app)
        self.limiter = limiter or TokenBucketRateLimiter()

    async def dispatch(self, request: Request, call_next):
        if request.url.path in ("/api/health", "/health", "/docs", "/openapi.json"):
            return await call_next(request)

        allowed, headers = self.limiter.check(request)
        if not allowed:
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Too Many Requests",
                    "message": "Rate limit exceeded. Please throttle your requests.",
                    "limit": headers.get("X-RateLimit-Limit"),
                    "retry_after_seconds": headers.get("Retry-After"),
                },
                headers=headers,
            )

        response = await call_next(request)
        for k, v in headers.items():
            response.headers[k] = v
        return response
