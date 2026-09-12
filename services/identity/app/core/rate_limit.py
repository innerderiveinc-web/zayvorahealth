from __future__ import annotations

import time
from collections import defaultdict, deque

from fastapi import HTTPException


class RateLimiter:
    """Sliding-window rate limiter supporting both Redis and in-memory backends.

    When redis_url is provided and reachable, it uses atomic Redis sorted set
    operations (ZADD, ZREMRANGEBYSCORE, ZCARD, EXPIRE) to share rate limit
    counters across all service replicas. If Redis is unconfigured or unreachable,
    it falls back cleanly to the local in-process sliding window.
    """

    def __init__(self, redis_url: str | None = None) -> None:
        self._hits: dict[str, deque] = defaultdict(deque)
        self._redis = None
        if redis_url:
            try:
                import redis

                self._redis = redis.from_url(redis_url, decode_responses=True)
                self._redis.ping()
            except Exception:
                self._redis = None

    def check(self, *, key: str, limit: int, window_seconds: int) -> None:
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
                    raise HTTPException(status_code=429, detail="Too many attempts. Please try again later.")
                return
            except HTTPException:
                raise
            except Exception:
                pass  # Redis transient error: fall back to local in-memory deque

        bucket = self._hits[key]
        while bucket and now - bucket[0] > window_seconds:
            bucket.popleft()
        if len(bucket) >= limit:
            raise HTTPException(status_code=429, detail="Too many attempts. Please try again later.")
        bucket.append(now)

    def reset(self, key: str) -> None:
        if self._redis is not None:
            try:
                self._redis.delete(f"rl:{key}")
            except Exception:
                pass
        self._hits.pop(key, None)
