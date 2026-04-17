# Student Assistant - Trợ lý Sinh viên AI

Chatbot hỗ trợ sinh viên tra cứu thông tin học vụ, sử dụng kiến trúc **LangGraph + LLM Router + RAG + Agent Tools**.

## Kiến trúc

```
User Query
    │
    ▼
LangGraph workflow
    │
    ├── route_query ───── Router LLM chọn nhánh/tool
    ├── run_rag ───────── Tài liệu nội bộ (quy chế, thông báo...)
    ├── collect_student_id
    │   ↳ interrupt nếu câu hỏi cá nhân chưa có MSSV
    ├── run_agent_tools ─ get_schedule() / get_grades() / get_exam() / get_tuition()
    └── finalize_response
```

Luồng chat mới:

1. Sinh viên hỏi tự do.
2. Backend gửi câu hỏi vào `LangGraph thread` theo `thread_id`.
3. Router xác định câu hỏi thuộc tài liệu nội bộ hay dữ liệu cá nhân.
4. Nếu là dữ liệu cá nhân mà chưa có `student_id`, graph sẽ `interrupt` để yêu cầu nhập MSSV.
5. Khi user gửi tin nhắn tiếp theo với cùng `thread_id`, graph tự resume và gọi tool tương ứng.

## Tech Stack

| Layer | Công nghệ |
|---|---|
| Backend | Python + FastAPI |
| Orchestration | LangGraph |
| LLM | OpenAI-compatible Chat API (`BASE_URL`, mặc định model `Minimax-M2.7`) |
| Embeddings | Jina AI (`jina-embeddings-v5-text-small`) |
| Vector DB | **FAISS** (lưu local trong project) |
| Frontend | Next.js 14 + React + Tailwind CSS |

## Cấu trúc Project

```
student_assistant/
├── backend/
│   └── app/
│       ├── main.py           # FastAPI app
│       ├── assistant_graph.py# LangGraph workflow chính
│       ├── router.py         # Router LLM (chỉ chọn tool/nhánh)
│       ├── config.py         # Cấu hình
│       ├── rag/
│       │   ├── ingestion.py  # Chunk + embed + lưu FAISS
│       │   ├── retrieval.py  # Vector search
│       │   └── generator.py  # Sinh câu trả lời có citation
│       ├── agents/
│       │   ├── tools.py      # Định nghĩa tool schemas
│       │   └── executor.py   # Thực thi tool + format kết quả
│       ├── fallback/
│       │   └── handler.py    # Xử lý câu hỏi ngoài phạm vi
│       └── mock_data/
│           ├── students.py   # DB sinh viên (lịch, điểm, lịch thi)
│           └── documents.py  # Tài liệu nội bộ
├── frontend/
│   └── src/app/
│       ├── page.tsx
│       └── components/
│           ├── Sidebar.tsx
│           ├── ChatWindow.tsx
│           ├── MessageBubble.tsx
│           └── ChatInput.tsx
├── data/
│   └── faiss_index/          # FAISS index (tự tạo khi chạy lần đầu)
├── requirements.txt
└── .env.example
```

## Cài đặt & Chạy

### 1. Backend

```bash
# Tạo và kích hoạt venv
python -m venv venv
./venv/Scripts/activate        # Windows
# source venv/bin/activate     # macOS/Linux

# Cài dependencies
pip install -r requirements.txt

# Tạo file .env
cp .env.example .env
# Điền OPENAI_API_KEY vào .env

# Chạy server
cd backend
uvicorn app.main:app --reload
# → http://localhost:8000
```

### Production local (Docker + Redis + Nginx)

```bash
cd student_assistant
docker compose up --build --scale agent=3
# → API qua Nginx: http://localhost:8080
```

Lần đầu chạy, server sẽ tự động **ingest tài liệu vào FAISS** (cần OpenAI API để embed). Các lần sau load từ disk, không cần embed lại.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
# → http://localhost:3000
```

## API

| Endpoint | Method | Mô tả |
|---|---|---|
| `/health` | GET | Health check |
| `/ready` | GET | Readiness check (Redis) |
| `/students` | GET | Danh sách sinh viên mock |
| `/chat` | POST | Gửi tin nhắn |

### Authentication (Part 6)

Tất cả endpoints (trừ `/health`, `/ready`) yêu cầu header `X-API-Key` phải trùng `AGENT_API_KEY` trong env.

**Request `/chat`:**
```json
{
  "thread_id": "8b20f5fa-3fb0-42cd-9f8b-d3fd876f5013",
  "message": "Lịch học tuần này của tôi như thế nào?"
}
```

**Response khi thiếu MSSV cho câu hỏi cá nhân:**
```json
{
  "thread_id": "8b20f5fa-3fb0-42cd-9f8b-d3fd876f5013",
  "response": "De minh tra cuu lich hoc cho ban, vui long nhap student id/MSSV (vi du: SV001).",
  "sources": [],
  "tool_used": "needs_student_id",
  "requires_student_id": true,
  "student_id": null
}
```

**Tin nhắn tiếp theo để resume cùng hội thoại:**
```json
{
  "thread_id": "8b20f5fa-3fb0-42cd-9f8b-d3fd876f5013",
  "message": "SV001"
}
```

## Test Cases

| Câu hỏi | Tool được gọi |
|---|---|
| "Quy chế đăng ký tín chỉ như thế nào?" | `RAG` |
| "Cho tôi xem lịch học tuần này" | `needs_student_id` → `get_schedule` |
| "Điểm môn Toán của tôi bao nhiêu?" | `needs_student_id` → `get_grades` |
| "Lịch thi cuối kỳ" | `needs_student_id` → `get_exam` |
| "Kiểm tra học phí của tôi" | `needs_student_id` → `get_tuition` |
| "Thời tiết hôm nay thế nào?" | `Fallback` |
| "Quy chế thi lại và lịch thi cuối kỳ" | `RAG + get_exam` |

## Mock Data

**Sinh viên:** SV001 (Nguyen Van An), SV002 (Tran Thi Bich), SV003 (Le Hoang Cuong)

**Tài liệu nội bộ:**
- Quy chế Đào tạo Tín chỉ
- Quy định Học phí và Miễn giảm
- Nội quy Thi cử và Kiểm tra
- Thông báo Học vụ HK2 2024-2025
- Hướng dẫn Sử dụng Hệ thống LMS
