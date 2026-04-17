from __future__ import annotations

import json
from typing import Any

from app import config
from app.redis_client import get_redis


def _thread_key(thread_id: str) -> str:
    return f"thread:{thread_id}"


def load_thread_state(thread_id: str) -> dict[str, Any]:
    r = get_redis()
    raw = r.get(_thread_key(thread_id))
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except Exception:
        return {}


def save_thread_state(thread_id: str, state: dict[str, Any]) -> None:
    r = get_redis()
    r.set(_thread_key(thread_id), json.dumps(state, ensure_ascii=False))


def append_history(thread_id: str, role: str, content: str) -> None:
    state = load_thread_state(thread_id)
    history: list[dict[str, str]] = list(state.get("history", []))
    history.append({"role": role, "content": content})
    max_len = int(config.MAX_THREAD_HISTORY_MESSAGES)
    if max_len > 0 and len(history) > max_len:
        history = history[-max_len:]
    state["history"] = history
    save_thread_state(thread_id, state)
