import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("BASE_URL")
JINA_API_KEY = os.getenv("JINA_API_KEY")
OPENAI_MODEL = "gpt-5.4-mini"
EMBEDDING_MODEL = "jina-embeddings-v5-text-small"
EMBEDDING_DIM = 1024

# Production settings (Part 6)
PORT = int(os.getenv("PORT", "8000"))
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
AGENT_API_KEY = os.getenv("AGENT_API_KEY", "")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "10"))
MONTHLY_BUDGET_USD = float(os.getenv("MONTHLY_BUDGET_USD", "10"))
COST_PER_REQUEST_USD = float(os.getenv("COST_PER_REQUEST_USD", "0.01"))
SESSION_TTL_SECONDS = int(os.getenv("SESSION_TTL_SECONDS", str(7 * 24 * 60 * 60)))
MAX_THREAD_HISTORY_MESSAGES = int(os.getenv("MAX_THREAD_HISTORY_MESSAGES", "50"))

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
FAISS_INDEX_DIR = os.path.join(ROOT_DIR, "data", "faiss_index")
UPLOAD_DIR = os.path.join(ROOT_DIR, "data", "uploads")
DOCUMENTS_META_PATH = os.path.join(ROOT_DIR, "data", "documents_meta.json")
RAG_TOP_K = 5
RAG_RELEVANCE_THRESHOLD = 0.5
