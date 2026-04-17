import re
from typing import Any, TypedDict

from app.agents.executor import execute_and_respond
from app.fallback.handler import get_fallback_response
from app.general.generator import generate_general_response, should_use_general_chat
from app.mock_data.students import get_student_info
from app.production.thread_store import append_history, load_thread_state, save_thread_state
from app.rag.generator import generate_rag_response
from app.rag.retrieval import retrieve
from app.router import detect_routes, get_search_query


class AssistantState(TypedDict, total=False):
    query: str
    student_id: str | None
    rag_calls: list[dict[str, Any]]
    agent_calls: list[dict[str, Any]]
    results: list[dict[str, Any]]
    response: str
    sources: list
    tool_used: str


TOOL_LABELS = {
    "get_schedule": "lịch học",
    "get_grades": "bảng điểm",
    "get_exam": "lịch thi",
    "get_tuition": "học phí",
}


def _combine_results(results: list[dict[str, Any]]) -> dict[str, Any]:
    if len(results) == 1:
        return results[0]

    combined_response = "\n\n---\n\n".join(result["response"] for result in results)
    all_sources: list = []
    all_tools: list[str] = []
    student_id = None

    for result in results:
        all_sources.extend(result.get("sources", []))
        if result.get("tool_used"):
            all_tools.extend(
                [part.strip() for part in result["tool_used"].split(",") if part.strip()]
            )
        if result.get("student_id"):
            student_id = result["student_id"]

    seen = set()
    unique_sources = []
    for src in all_sources:
        key = src["doc_id"] if isinstance(src, dict) else src
        if key not in seen:
            seen.add(key)
            unique_sources.append(src)

    return {
        "response": combined_response,
        "sources": unique_sources,
        "tool_used": ", ".join(dict.fromkeys(all_tools)),
        "student_id": student_id,
    }


def _extract_student_id(text: str) -> str:
    """Extract a student ID token from free-form text."""
    match = re.search(r"\b([A-Za-z]{1,4}\d{2,6})\b", text)
    if match:
        return match.group(1).upper()
    return text.strip().upper()


def _format_tool_list(tool_calls: list[dict[str, Any]]) -> str:
    labels = [TOOL_LABELS.get(tool_call["name"], tool_call["name"]) for tool_call in tool_calls]
    unique_labels = list(dict.fromkeys(labels))

    if not unique_labels:
        return "thông tin cá nhân"
    if len(unique_labels) == 1:
        return unique_labels[0]
    return ", ".join(unique_labels[:-1]) + f" và {unique_labels[-1]}"


def _build_student_id_prompt(
    state: AssistantState,
    invalid_student_id: str | None = None,
) -> dict[str, Any]:
    results = state.get("results", [])
    tool_text = _format_tool_list(state.get("agent_calls", []))

    if invalid_student_id:
        prompt = (
            f"Không tìm thấy sinh viên với mã số: {invalid_student_id}. "
            f"Vui lòng nhập lại MSSV hợp lệ để mình tra cứu {tool_text}. "
            "Bạn có thể dùng các mã demo như: SV001, SV002, SV003."
        )
    else:
        prompt = (
            f"Để mình tra cứu {tool_text} cho bạn, vui lòng cho mình biết MSSV "
            "(ví dụ: SV001)."
        )

    if results:
        combined = _combine_results(results)
        message = f"{combined['response']}\n\n---\n\n{prompt}"
        tools = [combined.get("tool_used", ""), "needs_student_id"]
        sources = combined.get("sources", [])
    else:
        message = prompt
        tools = ["needs_student_id"]
        sources = []

    tool_used = ", ".join(
        dict.fromkeys(
            part.strip()
            for tool_name in tools
            for part in tool_name.split(",")
            if part.strip()
        )
    )

    return {
        "message": message,
        "sources": sources,
        "tool_used": tool_used,
    }


def run_assistant_turn(
    thread_id: str, message: str, student_id: str | None = None
) -> dict[str, Any]:
    append_history(thread_id, "user", message)

    thread_state = load_thread_state(thread_id)
    pending: dict[str, Any] | None = thread_state.get("pending")

    # Resume flow when previous turn asked for student_id
    if pending and pending.get("requires_student_id"):
        extracted = _extract_student_id(message)
        if not get_student_info(extracted):
            prompt = _build_student_id_prompt(
                {
                    "results": pending.get("results", []),
                    "agent_calls": pending.get("agent_calls", []),
                },
                invalid_student_id=extracted,
            )
            response_text = prompt["message"]
            append_history(thread_id, "assistant", response_text)
            return {
                "response": response_text,
                "sources": prompt.get("sources", []),
                "tool_used": prompt.get("tool_used", "needs_student_id"),
                "requires_student_id": True,
                "student_id": None,
                "thread_id": thread_id,
            }

        # Valid student_id -> continue pending tools
        query = str(pending.get("query", ""))
        results = list(pending.get("results", []))
        agent_calls = list(pending.get("agent_calls", []))

        if agent_calls:
            results.append(execute_and_respond(agent_calls, query, extracted))

        thread_state["student_id"] = extracted
        thread_state["pending"] = None
        save_thread_state(thread_id, thread_state)

        combined = _combine_results(results) if results else None
        if combined:
            response_text = combined["response"]
            sources = combined.get("sources", [])
            tool_used = combined.get("tool_used", "unknown")
        else:
            response_text = get_fallback_response()["response"]
            sources = []
            tool_used = "fallback"

        append_history(thread_id, "assistant", response_text)
        return {
            "response": response_text,
            "sources": sources,
            "tool_used": tool_used,
            "requires_student_id": False,
            "student_id": extracted,
            "thread_id": thread_id,
        }

    # New query flow
    effective_student_id = student_id or thread_state.get("student_id")
    query = message

    route_result = detect_routes(query)
    rag_calls = route_result.get("rag_calls", [])
    agent_calls = route_result.get("agent_calls", [])
    results: list[dict[str, Any]] = []

    for rag_call in rag_calls:
        search_query = get_search_query(rag_call, query)
        chunks = retrieve(search_query)
        rag_result = generate_rag_response(search_query, chunks)
        if rag_result:
            results.append(rag_result)

    needs_student_id = bool(agent_calls) and not (
        effective_student_id and get_student_info(str(effective_student_id))
    )

    if needs_student_id:
        prompt = _build_student_id_prompt(
            {"results": results, "agent_calls": agent_calls},
        )
        thread_state["pending"] = {
            "requires_student_id": True,
            "query": query,
            "results": results,
            "agent_calls": agent_calls,
        }
        save_thread_state(thread_id, thread_state)

        response_text = prompt["message"]
        append_history(thread_id, "assistant", response_text)
        return {
            "response": response_text,
            "sources": prompt.get("sources", []),
            "tool_used": prompt.get("tool_used", "needs_student_id"),
            "requires_student_id": True,
            "student_id": None,
            "thread_id": thread_id,
        }

    if agent_calls and effective_student_id:
        results.append(execute_and_respond(agent_calls, query, str(effective_student_id)))

    if not results:
        if should_use_general_chat(query):
            gen = generate_general_response(query)
            response_text = gen["response"]
            sources = gen.get("sources", [])
            tool_used = gen.get("tool_used", "general")
        else:
            fallback = get_fallback_response()
            response_text = fallback["response"]
            sources = fallback.get("sources", [])
            tool_used = fallback.get("tool_used", "fallback")
    else:
        combined = _combine_results(results)
        response_text = combined["response"]
        sources = combined.get("sources", [])
        tool_used = combined.get("tool_used", "unknown")

    if effective_student_id:
        thread_state["student_id"] = str(effective_student_id)
        save_thread_state(thread_id, thread_state)

    append_history(thread_id, "assistant", response_text)
    return {
        "response": response_text,
        "sources": sources,
        "tool_used": tool_used,
        "requires_student_id": False,
        "student_id": effective_student_id,
        "thread_id": thread_id,
    }
