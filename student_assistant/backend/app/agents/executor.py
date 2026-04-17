import json
from datetime import datetime
from typing import Any

from openai import OpenAI

from app.config import OPENAI_API_KEY, OPENAI_MODEL, BASE_URL
from app.mock_data.students import get_schedule, get_grades, get_exam, get_tuition
from app.system_prompts import AGENT_RESPONSE_SYSTEM_PROMPT
from app.text_utils import clean_response_text

client = OpenAI(api_key=OPENAI_API_KEY, base_url=BASE_URL)

_WEEKDAY_VI = {0: "Thứ 2", 1: "Thứ 3", 2: "Thứ 4", 3: "Thứ 5", 4: "Thứ 6", 5: "Thứ 7", 6: "Chủ nhật"}


def _today_context() -> str:
    today = datetime.now()
    return f"Hôm nay là {_WEEKDAY_VI[today.weekday()]}, ngày {today.strftime('%d/%m/%Y')}."

TOOL_FUNCTIONS = {
    "get_schedule": get_schedule,
    "get_grades": get_grades,
    "get_exam": get_exam,
    "get_tuition": get_tuition,
}


def normalize_tool_calls(tool_calls: list[Any]) -> list[dict[str, Any]]:
    """Convert OpenAI tool calls or plain dicts into a normalized shape."""
    normalized = []

    for tool_call in tool_calls:
        if isinstance(tool_call, dict):
            name = tool_call.get("name")
            arguments = tool_call.get("arguments", {}) or {}
        else:
            name = tool_call.function.name
            raw_arguments = tool_call.function.arguments or "{}"
            arguments = json.loads(raw_arguments)

        normalized.append(
            {
                "name": name,
                "arguments": dict(arguments),
            }
        )

    return normalized


def execute_tool(tool_name: str, arguments: dict) -> dict:
    """Execute a single agent tool and return formatted results."""
    func = TOOL_FUNCTIONS.get(tool_name)
    if not func:
        return {"error": f"Unknown tool: {tool_name}"}

    result = func(**arguments)

    if result is None:
        return {"error": f"Khong tim thay sinh vien voi ma so: {arguments.get('student_id', 'N/A')}"}

    return {"data": result, "tool": tool_name}


def format_currency(value: int | float) -> str:
    return f"{int(value):,}".replace(",", ".") + " VND"


def format_tool_result(tool_name: str, result: dict) -> str:
    """Format tool execution result into a readable string."""
    if "error" in result:
        return result["error"]

    data = result["data"]

    if tool_name == "get_schedule":
        if not data:
            return "Khong co lich hoc nao."
        lines = ["LICH HOC TUAN NAY:"]
        for item in data:
            lines.append(f"- {item['day']} | {item['time']} | {item['subject']} | Phong {item['room']} | {item['teacher']}")
        return "\n".join(lines)

    if tool_name == "get_grades":
        if not data:
            return "Khong co du lieu diem."
        if isinstance(data, dict):
            lines = ["BANG DIEM:"]
            for semester, grades in data.items():
                lines.append(f"\n--- {semester} ---")
                for g in grades:
                    final_str = f"{g['final']}" if g["final"] is not None else "Chua co"
                    gpa_str = f"{g['gpa']}" if g["gpa"] is not None else "Chua co"
                    lines.append(f"- {g['subject']} ({g['credits']} TC) | Giua ky: {g['midterm']} | Cuoi ky: {final_str} | Diem HP: {gpa_str}")
            return "\n".join(lines)

        lines = ["BANG DIEM:"]
        for g in data:
            final_str = f"{g['final']}" if g["final"] is not None else "Chua co"
            gpa_str = f"{g['gpa']}" if g["gpa"] is not None else "Chua co"
            lines.append(f"- {g['subject']} ({g['credits']} TC) | Giua ky: {g['midterm']} | Cuoi ky: {final_str} | Diem HP: {gpa_str}")
        return "\n".join(lines)

    if tool_name == "get_exam":
        if not data:
            return "Khong co lich thi nao."
        lines = ["LICH THI CUOI KY:"]
        for item in data:
            lines.append(f"- {item['subject']} | Ngay: {item['date']} | {item['time']} | Phong: {item['room']} | Hinh thuc: {item['format']}")
        return "\n".join(lines)

    if tool_name == "get_tuition":
        if not data:
            return "Khong co du lieu hoc phi."
        lines = [
            "THONG TIN HOC PHI:",
            f"- Hoc ky: {data['semester']}",
            f"- So tin chi: {data['credits']} TC",
            f"- Don gia: {format_currency(data['unit_price'])}/tin chi",
            f"- Tam tinh: {format_currency(data['subtotal'])}",
            f"- Mien giam: {data['discount_percent']}% ({format_currency(data['discount_amount'])})",
            f"- Tong phai dong: {format_currency(data['total_due'])}",
            f"- Da dong: {format_currency(data['paid_amount'])}",
            f"- Con no: {format_currency(data['outstanding_amount'])}",
            f"- Han dong: {data['due_date']}",
            f"- Trang thai: {data['status']}",
        ]
        return "\n".join(lines)

    return json.dumps(data, ensure_ascii=False, indent=2)


def execute_tools_only(tool_calls: list[Any], query: str, student_id: str) -> dict:
    """Execute tools and prepare LLM messages without calling the LLM."""
    tool_results = []
    tools_used = []

    for tool_call in normalize_tool_calls(tool_calls):
        func_name = tool_call["name"]
        arguments = dict(tool_call.get("arguments", {}))

        if func_name in TOOL_FUNCTIONS:
            arguments["student_id"] = student_id

        result = execute_tool(func_name, arguments)
        formatted = format_tool_result(func_name, result)
        tool_results.append({"tool": func_name, "result": formatted})
        tools_used.append(func_name)

    combined_results = "\n\n".join(
        f"[Ket qua tu {tr['tool']}]\n{tr['result']}" for tr in tool_results
    )

    messages = [
        {
            "role": "system",
            "content": AGENT_RESPONSE_SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": f"{_today_context()}\n\nDỮ LIỆU SINH VIÊN:\n{combined_results}\n\n---\n\nCÂU HỎI: {query}",
        },
    ]

    return {
        "messages": messages,
        "tools_used": tools_used,
        "student_id": student_id,
    }


def execute_and_respond(tool_calls: list[Any], query: str, student_id: str) -> dict:
    """Execute all tool calls and generate a natural language response."""
    prepared = execute_tools_only(tool_calls, query, student_id)

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=prepared["messages"],
        temperature=0.3,
        max_completion_tokens=1000,
    )

    return {
        "response": clean_response_text(response.choices[0].message.content),
        "sources": [],
        "tool_used": ", ".join(prepared["tools_used"]),
        "student_id": student_id,
    }
