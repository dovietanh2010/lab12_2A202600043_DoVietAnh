from __future__ import annotations

import redis

from app import config


_client: redis.Redis | None = None


def get_redis() -> redis.Redis:
    global _client
    if _client is None:
        _client = redis.from_url(config.REDIS_URL, decode_responses=True)
    return _client


def close_redis() -> None:
    global _client
    if _client is None:
        return
    try:
        _client.close()
    finally:
        _client = None
