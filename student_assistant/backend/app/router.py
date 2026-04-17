import json
from typing import Any

from openai import OpenAI

from app.config import OPENAI_API_KEY, OPENAI_MODEL, BASE_URL
from app.agents.tools import get_all_tools
from app.agents.executor import normalize_tool_calls
from app.system_prompts import ROUTER_SYSTEM_PROMPT

client = OpenAI(api_key=OPENAI_API_KEY, base_url=BASE_URL)


def detect_routes(query: str) -> dict[str, Any]:
    """Ask the LLM router which branch or tools should handle the query."""
    tools = get_all_tools()

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": ROUTER_SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ],
        tools=tools,
        tool_choice="auto",
        temperature=0,
    )

    message = response.choices[0].message
    if not message.tool_calls:
        return {
            "rag_calls": [],
            "agent_calls": [],
            "is_fallback": True,
        }

    rag_calls = []
    agent_calls = []

    for tool_call in normalize_tool_calls(message.tool_calls):
        if tool_call["name"] == "search_documents":
            rag_calls.append(tool_call)
        else:
            agent_calls.append(tool_call)

    return {
        "rag_calls": rag_calls,
        "agent_calls": agent_calls,
        "is_fallback": False,
    }


def get_search_query(tool_call: dict[str, Any], default_query: str) -> str:
    """Extract the search query for the RAG tool."""
    arguments = tool_call.get("arguments", {})
    return str(arguments.get("query", default_query))
