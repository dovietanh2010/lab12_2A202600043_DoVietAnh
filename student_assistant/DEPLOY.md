# Deploy guide (Render / Railway)

Thư mục deploy: `student_assistant/`

## 0) Chuẩn bị

- App chạy HTTP trên port `8000` trong container (`Dockerfile` đã cấu hình).
- Reverse proxy/load balancer (nginx) chỉ dùng khi chạy local bằng `docker compose`.
- Khi deploy cloud, bạn chỉ cần deploy **một** service `agent` + **một** Redis.

## 1) Environment variables (bắt buộc)

Thiết lập cho service `agent`:

- `PORT=8000`
- `REDIS_URL=redis://...` (lấy từ Redis provider)
- `AGENT_API_KEY=your-secret`

## 2) Environment variables (khuyến nghị)

- `LOG_LEVEL=INFO`
- `RATE_LIMIT_PER_MINUTE=10`
- `MONTHLY_BUDGET_USD=10`
- `COST_PER_REQUEST_USD=0.01`
- `SESSION_TTL_SECONDS=604800`
- `MAX_THREAD_HISTORY_MESSAGES=50`

Tuỳ chọn (nếu dùng OpenAI thật):
- `OPENAI_API_KEY=...`
- `BASE_URL=...` (nếu dùng proxy/base url khác)

## 3) Deploy lên Railway

1. Tạo project mới trên Railway.
2. Add **Redis** (Railway add-on) → copy `REDIS_URL`.
3. Add **Service** từ GitHub repo:
   - Root directory: `student_assistant`
   - Build: dùng `Dockerfile`
4. Set variables theo mục (1)(2).
5. Deploy và mở public domain.

Test nhanh:

```bash
curl -i https://YOUR_DOMAIN/health
curl -i https://YOUR_DOMAIN/ready
curl -i -X POST https://YOUR_DOMAIN/auth/login ^
  -H "Content-Type: application/json" ^
  -H "X-API-Key: your-secret" ^
  -d "{\"username\":\"admin\",\"password\":\"admin\"}"
```

## 4) Deploy lên Render

1. Tạo **Redis** trên Render trước → copy `REDIS_URL`.
2. Tạo **Web Service** từ GitHub repo:
   - Root directory: `student_assistant`
   - Environment: **Docker**
3. Set variables theo mục (1)(2).
4. Deploy và mở public URL.

Test nhanh (giống Railway):

```bash
curl -i https://YOUR_DOMAIN/health
curl -i https://YOUR_DOMAIN/ready
```

## 5) Checklist khi nộp bài

- Có public URL chạy được.
- `GET /health` trả `200`.
- `GET /ready` trả `200` (Redis sẵn sàng).
- API yêu cầu key: thiếu `X-API-Key` phải trả `401`.
- Rate limit: vượt `RATE_LIMIT_PER_MINUTE` trả `429`.
- Cost guard: vượt `MONTHLY_BUDGET_USD` trả `402`.

