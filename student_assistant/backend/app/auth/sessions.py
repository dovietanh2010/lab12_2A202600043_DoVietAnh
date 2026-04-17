import secrets
import json

from fastapi import Depends, Header, HTTPException, status

from app import config
from app.redis_client import get_redis


def create_session(user: dict) -> str:
    token = secrets.token_urlsafe(32)
    r = get_redis()
    key = f"session:{token}"
    r.set(key, json.dumps(dict(user), ensure_ascii=False))
    r.expire(key, config.SESSION_TTL_SECONDS)
    return token


def get_user_from_token(token: str) -> dict | None:
    r = get_redis()
    raw = r.get(f"session:{token}")
    if not raw:
        return None
    try:
        return json.loads(raw)
    except Exception:
        return None


def get_current_user(authorization: str | None = Header(default=None)) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Thiếu thông tin xác thực",
        )

    token = authorization.split(" ", 1)[1].strip()
    user = get_user_from_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Phiên đăng nhập không hợp lệ hoặc đã hết hạn",
        )

    return user


def require_admin(current_user: dict = Depends(get_current_user)) -> dict:
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền truy cập chức năng này",
        )

    return current_user
