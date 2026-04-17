import re

from openai import OpenAI

from app.config import OPENAI_API_KEY, OPENAI_MODEL, BASE_URL
from app.system_prompts import GENERAL_CHAT_SYSTEM_PROMPT
from app.text_utils import clean_response_text, normalize_text_for_matching

client = OpenAI(api_key=OPENAI_API_KEY, base_url=BASE_URL)

GENERAL_CHAT_KEYWORDS = [
    "xin chao",
    "chao",
    "hello",
    "hi",
    "hey",
    "alo",
    "cam on",
    "cảm ơn",
    "thank you",
    "tam biet",
    "tạm biệt",
    "bye",
    "goodbye",
    "ban la ai",
    "bạn là ai",
    "ban ten gi",
    "bạn tên gì",
    "ban co the lam gi",
    "bạn có thể làm gì",
    "khoe khong",
    "khỏe không",
    "how are you",
]

GENERAL_CHAT_PATTERNS = [
    re.compile(r"\b(chao|xin chao|hello|hi|hey|alo)\b"),
    re.compile(r"\b(cam on|thank you|thanks)\b"),
    re.compile(r"\b(tam biet|bye|goodbye|hen gap lai)\b"),
    re.compile(r"\b(ban la ai|ban ten gi|ban co the lam gi)\b"),
    re.compile(r"\b(khoe khong|how are you)\b"),
]


def should_use_general_chat(query: str) -> bool:
    """Detect simple greetings and social chatter that should not hit fallback."""
    normalized = normalize_text_for_matching(query)
    if not normalized:
        return False

    if normalized in {"ok", "oke", "okela", "okie", "yes", "no", "uhm", "um", "dung roi"}:
        return True

    if any(keyword in normalized for keyword in GENERAL_CHAT_KEYWORDS):
        return True

    short_social_messages = {
        "chao ban",
        "cam on ban",
        "tam biet nha",
        "rat vui duoc gap ban",
        "ban oi",
    }
    if normalized in short_social_messages:
        return True

    if len(normalized.split()) <= 8 and any(pattern.search(normalized) for pattern in GENERAL_CHAT_PATTERNS):
        return True

    return False


def generate_general_response(query: str) -> dict:
    """Generate a natural conversational reply for small talk."""
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": GENERAL_CHAT_SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ],
        temperature=0.7,
        max_completion_tokens=300,
    )

    return {
        "response": clean_response_text(response.choices[0].message.content),
        "sources": [],
        "tool_used": "general_chat",
    }
