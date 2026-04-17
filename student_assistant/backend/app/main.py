import os
import uuid
from contextlib import asynccontextmanager
import json
import logging

from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.assistant_graph import run_assistant_turn
from app.auth.sessions import create_session, get_current_user, require_admin
from app.auth.users import authenticate
from app.config import UPLOAD_DIR
from app.redis_client import close_redis, get_redis
from app.documents.metadata_store import (
    add_document,
    get_all_documents as get_all_doc_meta,
    remove_document,
)
from app.documents.pdf_parser import extract_text_from_pdf
from app.mock_data.students import get_all_students
from app.production.api_key import verify_api_key
from app.production.cost_guard import check_budget
from app.production.rate_limiter import check_rate_limit
from app.rag.ingestion import (
    add_document_to_index,
    initialize_index,
    remove_document_from_index,
)


class LoginRequest(BaseModel):
    username: str
    password: str


class ChatRequest(BaseModel):
    thread_id: str
    message: str
    student_id: str | None = None


class ChatResponse(BaseModel):
    thread_id: str
    response: str
    sources: list
    tool_used: str
    requires_student_id: bool = False
    student_id: str | None = None


class StudentInfo(BaseModel):
    id: str
    name: str


class LoginResponse(BaseModel):
    username: str
    role: str
    display_name: str
    student_id: str | None = None
    token: str


os.makedirs(UPLOAD_DIR, exist_ok=True)


def _setup_json_logging() -> None:
    root = logging.getLogger()
    if root.handlers:
        return

    level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)

    handler = logging.StreamHandler()

    class JsonFormatter(logging.Formatter):
        def format(self, record: logging.LogRecord) -> str:
            payload = {
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
            }
            if record.exc_info:
                payload["exc_info"] = self.formatException(record.exc_info)
            return json.dumps(payload, ensure_ascii=False)

    handler.setFormatter(JsonFormatter())
    root.addHandler(handler)
    root.setLevel(level)


@asynccontextmanager
async def lifespan(app: FastAPI):
    _setup_json_logging()
    logger = logging.getLogger("app")

    logger.info("Initializing FAISS index...")
    initialize_index()
    logger.info("FAISS index ready. Server started.")
    yield
    close_redis()


app = FastAPI(
    title="Student Assistant API",
    description="API trợ lý sinh viên theo kiến trúc LangGraph + RAG + Agent Tools",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")


@app.post("/api/auth/login", response_model=LoginResponse)
def login(
    request: LoginRequest,
):
    user = authenticate(request.username, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Sai tên đăng nhập hoặc mật khẩu")
    
    try:
        token = create_session(user)
        return {**user, "token": token}
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Lỗi kết nối Redis: {str(e)}. Vui lòng kiểm tra cấu hình REDIS_URL trên Render."
        )


@app.get("/api/health")
async def health():
    return {"status": "ok"}


@app.get("/api/ready")
async def ready():
    try:
        get_redis().ping()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Redis chua san sang: {e}")
    return {"status": "ready"}


@app.get("/api/students", response_model=list[StudentInfo])
async def list_students(
    _api_key: None = Depends(verify_api_key),
    current_user: dict = Depends(require_admin),
):
    check_rate_limit(current_user["username"])
    check_budget(current_user["username"])
    students = get_all_students()
    return [StudentInfo(id=student["id"], name=student["name"]) for student in students]


@app.post("/api/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    _api_key: None = Depends(verify_api_key),
    current_user: dict = Depends(get_current_user),
):
    check_rate_limit(current_user["username"])
    check_budget(current_user["username"])

    effective_student_id = request.student_id
    if current_user["role"] == "student":
        effective_student_id = current_user.get("student_id")

    result = run_assistant_turn(
        request.thread_id, request.message, student_id=effective_student_id
    )

    return ChatResponse(
        thread_id=result["thread_id"],
        response=result["response"],
        sources=result.get("sources", []),
        tool_used=result.get("tool_used", "unknown"),
        requires_student_id=result.get("requires_student_id", False),
        student_id=result.get("student_id"),
    )


@app.get("/api/admin/documents")
def list_documents(
    _api_key: None = Depends(verify_api_key),
    current_user: dict = Depends(require_admin),
):
    check_rate_limit(current_user["username"])
    check_budget(current_user["username"])
    return get_all_doc_meta()


@app.post("/api/admin/documents/upload")
def upload_document(
    _api_key: None = Depends(verify_api_key),
    file: UploadFile = File(...),
    title: str = Form(None),
    category: str = Form("general"),
    current_user: dict = Depends(require_admin),
):
    check_rate_limit(current_user["username"])
    check_budget(current_user["username"])

    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Chỉ chấp nhận file PDF")

    doc_id = uuid.uuid4().hex[:12]
    file_path = os.path.join(UPLOAD_DIR, f"{doc_id}.pdf")

    content = file.file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    try:
        text, page_count = extract_text_from_pdf(file_path)
    except Exception as e:
        os.remove(file_path)
        raise HTTPException(status_code=400, detail=f"Không thể đọc file PDF: {e}")

    if not text.strip():
        os.remove(file_path)
        raise HTTPException(status_code=400, detail="File PDF không có nội dung text")

    doc_title = title or os.path.splitext(file.filename)[0]
    chunk_count = add_document_to_index(doc_id, doc_title, category, text)

    doc_meta = add_document(
        doc_id=doc_id,
        filename=file.filename,
        title=doc_title,
        category=category,
        page_count=page_count,
        chunk_count=chunk_count,
        uploaded_by=current_user["username"],
    )

    return doc_meta


@app.delete("/api/admin/documents/{doc_id}")
def delete_document(
    doc_id: str,
    _api_key: None = Depends(verify_api_key),
    current_user: dict = Depends(require_admin),
):
    check_rate_limit(current_user["username"])
    check_budget(current_user["username"])
    removed = remove_document(doc_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài liệu")

    remove_document_from_index(doc_id)

    file_path = os.path.join(UPLOAD_DIR, f"{doc_id}.pdf")
    if os.path.exists(file_path):
        os.remove(file_path)

    return {"message": "Đã xóa tài liệu", "doc_id": doc_id}

# --- UI Serving logic ---
# Current file is in student_assistant/backend/app/main.py
# static folder is at student_assistant/backend/static
current_dir = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(os.path.dirname(current_dir), "static")

# Mount static files at / (must be after defining API routes)
if os.path.exists(STATIC_DIR):
    app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")


# Catch-all for SPA (must be the VERY LAST handler)
@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    # Try to serve index.html for any route that doesn't start with /api or /uploads
    if not full_path.startswith("api/") and not full_path.startswith("uploads/"):
        index_path = os.path.join(STATIC_DIR, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
    raise HTTPException(status_code=404, detail="Not Found")
