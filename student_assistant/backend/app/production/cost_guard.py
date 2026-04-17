from __future__ import annotations

from datetime import datetime, timezone

from fastapi import HTTPException, status

from app import config
from app.redis_client import get_redis


def _month_key() -> str:
    now = datetime.now(timezone.utc)
    return f"{now.year:04d}-{now.month:02d}"


def check_budget(user_id: str) -> None:
    """
    Minimal cost guard:
    - Each request costs COST_PER_REQUEST_USD (configurable)
    - Track per-user per-month spend in Redis
    """
    r = get_redis()
    month = _month_key()
    key = f"cost:{user_id}:{month}"

    new_total = r.incrbyfloat(key, float(config.COST_PER_REQUEST_USD))
    # Keep keys for ~90 days to cover late reads/debugging
    r.expire(key, 90 * 24 * 60 * 60)

    if float(new_total) > float(config.MONTHLY_BUDGET_USD):
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Vượt ngân sách tháng, vui lòng nâng hạn mức hoặc thử lại tháng sau",
        )
