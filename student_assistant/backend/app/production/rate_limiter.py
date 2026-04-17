from __future__ import annotations

import time

from fastapi import HTTPException, status

from app import config
from app.redis_client import get_redis


def check_rate_limit(user_id: str) -> None:
    """
    Sliding window rate limit using Redis ZSET:
    - Keep timestamps in the last 60s
    - Reject if count > RATE_LIMIT_PER_MINUTE
    """
    r = get_redis()
    now_ms = int(time.time() * 1000)
    window_ms = 60_000
    key = f"ratelimit:{user_id}"

    pipe = r.pipeline(transaction=True)
    pipe.zremrangebyscore(key, 0, now_ms - window_ms)
    pipe.zadd(key, {str(now_ms): now_ms})
    pipe.zcard(key)
    pipe.pexpire(key, window_ms + 5_000)
    _, _, count, _ = pipe.execute()

    if int(count) > config.RATE_LIMIT_PER_MINUTE:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="QuÃ¡ nhiá»u yÃªu cáº§u, vui lÃ²ng thá»­ láº¡i sau",
        )
