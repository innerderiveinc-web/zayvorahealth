"""
Rate limiting utilities for the ZAYVORA Identity service (Phase 2 hardening).

Provides:
- ``RateLimiter``          – sliding-window limiter (IP-based and per-user).
                             Supports Redis-backed distributed counting with
                             in-process fallback for single-instance deployments.
- ``LoginLockoutManager``  – tracks failed login attempts per identifier and
                             locks out callers after ``max_attempts`` failures.
                             Lockout state is stored in Redis (with TTL) when
                             available, falling back to an in-process dict.

SlowAPI integration notes
-------------------------
The helpers below are compatible with FastAPI + ``slowapi``.  When using
slowapi's ``@limiter.limit(...)`` decorator you can still call
``RateLimiter.check()`` manually for fine-grained control or combined
IP + user-level limits.
"""
from __future__ import annotations

import time
from collections import defaultdict, deque
from typing import Optional

from fastapi import HTTPException


class RateLimiter:
    """Sliding-window rate limiter supporting both Redis and in-memory backends.

    When *redis_url* is provided and reachable, it uses atomic Redis sorted set
    operations (ZADD, ZREMRANGEBYSCORE, ZCARD, EXPIRE) to share rate limit
    counters across all service replicas.  If Redis is unconfigured or
    unreachable it falls back cleanly to the local in-process sliding window.

    IP-based limiting example::

        limiter = RateLimiter(redis_url=settings.redis_url)
        limiter.check(key=f"ip:{client_ip}", limit=60, window_seconds=60)

    Per-user limiting example::

        limiter.check(key=f"user:{user_id}", limit=300, window_seconds=60)
    """

    def __init__(self, redis_url: Optional[str] = None) -> None:
        self._hits: dict[str, deque] = defaultdict(deque)
        self._redis = None
        if redis_url:
            try:
                import redis

                self._redis = redis.from_url(redis_url, decode_responses=True)
                self._redis.ping()
            except Exception:
                self._redis = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def check(self, *, key: str, limit: int, window_seconds: int) -> None:
        """Assert that *key* has not exceeded *limit* hits in the past *window_seconds*.

        Args:
            key:            Arbitrary string identifying the rate-limited entity,
                            e.g. ``"ip:203.0.113.5"`` or ``"user:abc-123"``.
            limit:          Maximum number of allowed requests in the window.
            window_seconds: Length of the sliding window in seconds.

        Raises:
            HTTPException(429): When the limit has been exceeded.
        """
        now = time.time()
        if self._redis is not None:
            try:
                redis_key = f"rl:{key}"
                pipe = self._redis.pipeline()
                pipe.zremrangebyscore(redis_key, 0, now - window_seconds)
                pipe.zcard(redis_key)
                pipe.zadd(redis_key, {str(now): now})
                pipe.expire(redis_key, window_seconds + 1)
                _, count, _, _ = pipe.execute()
                if count >= limit:
                    raise HTTPException(
                        status_code=429,
                        detail="Too many attempts. Please try again later.",
                    )
                return
            except HTTPException:
                raise
            except Exception:
                pass  # Redis transient error – fall back to local in-memory deque

        bucket = self._hits[key]
        while bucket and now - bucket[0] > window_seconds:
            bucket.popleft()
        if len(bucket) >= limit:
            raise HTTPException(
                status_code=429,
                detail="Too many attempts. Please try again later.",
            )
        bucket.append(now)

    def check_ip(self, ip: str, *, limit: int = 60, window_seconds: int = 60) -> None:
        """Convenience wrapper for IP-address based rate limiting.

        Args:
            ip:             Client IP address string.
            limit:          Max requests per window. Defaults to 60.
            window_seconds: Window size in seconds. Defaults to 60.
        """
        self.check(key=f"ip:{ip}", limit=limit, window_seconds=window_seconds)

    def check_user(self, user_id: str, *, limit: int = 300, window_seconds: int = 60) -> None:
        """Convenience wrapper for per-user authenticated rate limiting.

        Args:
            user_id:        Opaque user identifier (UUID string recommended).
            limit:          Max requests per window. Defaults to 300.
            window_seconds: Window size in seconds. Defaults to 60.
        """
        self.check(key=f"user:{user_id}", limit=limit, window_seconds=window_seconds)

    def reset(self, key: str) -> None:
        """Clear the rate-limit counter for *key* (e.g. after a successful login).

        Args:
            key: Same key string used in ``check()``.
        """
        if self._redis is not None:
            try:
                self._redis.delete(f"rl:{key}")
            except Exception:
                pass
        self._hits.pop(key, None)


class LoginLockoutManager:
    """Tracks failed login attempts and enforces account lockout.

    After ``max_attempts`` consecutive failures for a given identifier (email
    or IP), the account is locked for ``lockout_seconds``.  On a successful
    authentication call ``record_success()`` to reset the counter.

    State is stored in Redis when available (recommended for multi-replica
    deployments), with a process-local dict as a fallback.

    Usage::

        lockout = LoginLockoutManager(
            redis_url=settings.redis_url,
            max_attempts=5,
            lockout_seconds=900,  # 15 minutes
        )

        # On every login attempt:
        lockout.check(identifier=email)      # raises 429 if locked out
        try:
            ...authenticate...
            lockout.record_success(email)
        except AuthError:
            lockout.record_failure(email)
            raise
    """

    def __init__(
        self,
        redis_url: Optional[str] = None,
        *,
        max_attempts: int = 5,
        lockout_seconds: int = 900,
    ) -> None:
        self._max_attempts = max_attempts
        self._lockout_seconds = lockout_seconds
        # In-process fallback: identifier -> (failure_count, lockout_until_ts)
        self._state: dict[str, tuple[int, float]] = {}
        self._redis = None
        if redis_url:
            try:
                import redis

                self._redis = redis.from_url(redis_url, decode_responses=True)
                self._redis.ping()
            except Exception:
                self._redis = None

    # Redis key helpers
    def _fail_key(self, identifier: str) -> str:
        return f"login_fail:{identifier}"

    def _lock_key(self, identifier: str) -> str:
        return f"login_lock:{identifier}"

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def check(self, identifier: str) -> None:
        """Raise HTTP 429 if *identifier* is currently locked out.

        Args:
            identifier: Typically the user's email address or client IP.

        Raises:
            HTTPException(429): When the identifier is locked out.
        """
        if self._redis is not None:
            try:
                if self._redis.exists(self._lock_key(identifier)):
                    ttl = self._redis.ttl(self._lock_key(identifier))
                    raise HTTPException(
                        status_code=429,
                        detail=(
                            f"Account temporarily locked due to too many failed login attempts. "
                            f"Try again in {max(ttl, 1)} seconds."
                        ),
                    )
                return
            except HTTPException:
                raise
            except Exception:
                pass

        _count, locked_until = self._state.get(identifier, (0, 0.0))
        if locked_until > time.time():
            wait = int(locked_until - time.time())
            raise HTTPException(
                status_code=429,
                detail=(
                    f"Account temporarily locked due to too many failed login attempts. "
                    f"Try again in {wait} seconds."
                ),
            )

    def record_failure(self, identifier: str) -> None:
        """Increment the failure counter and lock the account if the threshold is reached.

        Args:
            identifier: Typically the user's email address or client IP.
        """
        if self._redis is not None:
            try:
                fail_key = self._fail_key(identifier)
                count = self._redis.incr(fail_key)
                self._redis.expire(fail_key, self._lockout_seconds)
                if count >= self._max_attempts:
                    self._redis.setex(
                        self._lock_key(identifier), self._lockout_seconds, "1"
                    )
                return
            except Exception:
                pass

        count, locked_until = self._state.get(identifier, (0, 0.0))
        count += 1
        new_locked_until = (
            time.time() + self._lockout_seconds if count >= self._max_attempts else locked_until
        )
        self._state[identifier] = (count, new_locked_until)

    def record_success(self, identifier: str) -> None:
        """Reset failure counters after a successful authentication.

        Args:
            identifier: Typically the user's email address or client IP.
        """
        if self._redis is not None:
            try:
                self._redis.delete(self._fail_key(identifier))
                self._redis.delete(self._lock_key(identifier))
            except Exception:
                pass
        self._state.pop(identifier, None)
