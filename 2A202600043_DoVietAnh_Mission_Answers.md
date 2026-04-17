# Day 12 Lab - Mission Answers

## Part 1: Localhost vs Production

### Exercise 1.1: Anti-patterns found
1. **Hardcoded Secrets**: API Key và Database URL được viết trực tiếp vào mã nguồn, gây rủi ro bảo mật lớn nếu lộ code.
2. **Missing Config Management**: Các thông số cấu hình như `DEBUG` và `MAX_TOKENS` bị fix cứng, khó thay đổi linh hoạt giữa các môi trường.
3. **Inappropriate Logging**: Sử dụng `print()` thay vì hệ thống logging chuyên nghiệp. Điều này dẫn đến lỗi Unicode (như bạn vừa thấy ở terminal) và rủi ro lộ dữ liệu nhạy cảm.
4. **No Health Check Endpoints**: Thiếu các endpoint `/health` và `/ready` khiến hệ thống giám sát không thể biết Agent còn sống hay không.
5. **Fixed Port and Host**: App bị fix cứng ở `localhost:8000`, không thể chạy được trên Docker hoặc Cloud (vốn cần `0.0.0.0` và Port động).

### Exercise 1.3: Comparison table

| Feature | Basic (Develop) | Advanced (Production) | Why Important? |
|---------|-----------------|-----------------------|----------------|
| **Config** | Hardcoded trong `app.py` | Tách biệt ra file `config.py` | Bảo mật và linh hoạt giữa các môi trường (Dev/Prod). |
| **Health Check** | Không có | Có `/health` và `/ready` | Giúp Cloud platform tự động restart nếu app bị treo. |
| **Logging** | `print()` (Không cấu trúc) | Structured JSON Logging | Dễ quản lý log, tránh lỗi encoding, không lộ secret. |
| **Shutdown** | Tắt đột ngột | Graceful (Xử lý SIGTERM) | Đảm bảo các request đang chạy được hoàn thành trước khi đóng. |
| **Binding** | `localhost:8000` | `0.0.0.0` + dynamic `PORT` | Bắt buộc để chạy được trên Docker và các nền tảng Cloud. |

---

## Part 2: Docker

### Exercise 2.1: Dockerfile questions
1. **Base image là gì?**: image nền chứa sẵn Python 3.11 để build container `python:3.11` (Bản đầy đủ, dung lượng lớn).
2. **Working directory là gì?**: `/app` (Thư mục làm việc chính bên trong container).
3. **Tại sao COPY requirements.txt trước?**: Để tận dụng **Docker Layer Caching**. Nếu file requirements không đổi, Docker sẽ dùng lại layer đã cài đặt dependencies, giúp build nhanh hơn rất nhiều ở các lần sau.
4. **CMD vs ENTRYPOINT khác nhau thế nào?**:
    *   `CMD`: Thiết lập lệnh mặc định, có thể dễ dàng bị ghi đè khi chạy lệnh `docker run`.
    *   `ENTRYPOINT`: Thiết lập lệnh chính sẽ chạy, khó bị ghi đè hơn và thường được dùng để biến container thành một file thực thi. Ở đây dùng `CMD` để linh hoạt hơn.

### Exercise 2.3: Image size comparison
- Develop: 1.66 GB
- Production: 236MB
- Difference: Giảm ~85%

### Exercise 2.4: Docker Compose questions
1. **Services nào được start?**: Agent, Redis và Nginx.
2. **Chúng communicate thế nào?**: Thông qua mạng nội bộ của Docker (Docker bridge network). Nginx đóng vai trò là cổng vào (Reverse Proxy), điều hướng yêu cầu đến Agent. Agent kết nối với Redis để lưu trữ dữ liệu.

### Discussion Questions
1. **Tại sao COPY requirements.txt trước?**: Để tận dụng cache. Nếu code thay đổi nhưng thư viện không đổi, Docker sẽ không phải cài lại thư viện, giúp tiết kiệm thời gian build.
2. **.dockerignore nên chứa những gì?**: Các file không cần thiết như `__pycache__`, `.git`, `venv`, và đặc biệt là file bí mật `.env`. Việc này giúp image nhẹ hơn và an toàn hơn.
3. **Làm sao mount volume?**: Sử dụng flag `-v` khi chạy lệnh `docker run` hoặc khai báo `volumes` trong file `docker-compose.yml`.


## Part 3: Cloud Deployment

### Exercise 3.1: Cloud Deployment (Railway & Render)
- **Public URL (Railway)**: https://lab12part3-production.up.railway.app/
- **Snapshot**: pics/deploy_part3.png
- **Public URL (Render)**: https://ai-agent-1oa6.onrender.com/
- **Snapshot**: pics/deploy_part3_2.png
- **Platform**: Railway / Render
- **Cách thực hiện**:
    *   **Railway**: Dùng Railway CLI (`railway up`) để deploy nhanh từ terminal.
    *   **Render**: Dùng file `render.yaml` (Blueprint) kết nối với GitHub để tự động hóa hạ tầng (IaC).

Ghi chú: Hướng dẫn deploy chi tiết đã được viết tại `student_assistant/DEPLOY.md`.

### Exercise 3.2: Compare config files
- **`railway.toml` vs `render.yaml`**:
    *   **`railway.toml`**: Đơn giản, tập trung vào lệnh chạy (`startCommand`) và cách build. Phù hợp cho các ứng dụng nhỏ, cần deploy nhanh.
    *   **`render.yaml`**: Mạnh mẽ hơn, cho phép định nghĩa nhiều dịch vụ (Web, Redis, DB) cùng lúc. Đây là mô hình **Infrastructure as Code**, giúp quản lý toàn bộ hệ thống chuyên nghiệp và dễ tái sử dụng.

---

## Part 4: API Security

### Exercise 4.1-4.3: Test results

#### 1. Kiểm tra API Key (X-API-Key Authentication)
Hệ thống yêu cầu header `X-API-Key` cho các endpoint nhạy cảm (như `/api/chat`, `/api/admin/*`).
- **Output**: `{"detail": "Missing API key. Include header: X-API-Key: <your-key>"}`
- **Output**: `{"detail": "Invalid API key."}`


#### 2. Kiểm tra JWT Authentication (Token-based Session)
Người dùng đăng nhập để lấy Session Token.
- **Login thành công**: `HTTP/1.1 200 OK` -> `{"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9eyJzdWIiOiJzdHVkZW50Iiwicm9sZSI6InVzZXIiLCJpYXQiOjE3NzY0NDMxNzUsImV4cCI6MTc3NjQ0Njc3NX0.-ekn2EkPPSS_fF2e4wY5xae8Cc6TvVbSz79FES36nr0",
"token_type": "bearer",
"expires_in_minutes": 60,
"hint": "Include in header: Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
}`
- **Sử dụng Token**: Gửi header `Authorization: Bearer <token>` để xác thực danh tính cho các tác vụ tiếp theo (Chat, Quản lý tài liệu).

#### 3. Kiểm tra Rate Limiting (Anti-spam)
Ngăn chặn người dùng gửi quá nhiều yêu cầu trong thời gian ngắn.
- **Output**: `INFO:cost_guard:Usage: user=student req=1 cost=$0.0000/1.0
INFO:     127.0.0.1:54347 - "POST /ask HTTP/1.1" 200 OK
INFO:cost_guard:Usage: user=student req=2 cost=$0.0000/1.0
INFO:     127.0.0.1:56370 - "POST /ask HTTP/1.1" 200 OK
INFO:cost_guard:Usage: user=student req=3 cost=$0.0001/1.0
INFO:     127.0.0.1:56370 - "POST /ask HTTP/1.1" 200 OK
INFO:cost_guard:Usage: user=student req=4 cost=$0.0001/1.0
INFO:     127.0.0.1:56370 - "POST /ask HTTP/1.1" 200 OK
INFO:cost_guard:Usage: user=student req=5 cost=$0.0001/1.0
INFO:     127.0.0.1:56370 - "POST /ask HTTP/1.1" 200 OK
INFO:cost_guard:Usage: user=student req=6 cost=$0.0001/1.0
INFO:     127.0.0.1:56370 - "POST /ask HTTP/1.1" 200 OK
INFO:cost_guard:Usage: user=student req=7 cost=$0.0001/1.0
INFO:     127.0.0.1:56370 - "POST /ask HTTP/1.1" 200 OK
INFO:cost_guard:Usage: user=student req=8 cost=$0.0002/1.0
INFO:     127.0.0.1:56370 - "POST /ask HTTP/1.1" 200 OK
INFO:cost_guard:Usage: user=student req=9 cost=$0.0002/1.0
INFO:     127.0.0.1:56370 - "POST /ask HTTP/1.1" 200 OK
INFO:cost_guard:Usage: user=student req=10 cost=$0.0002/1.0
INFO:     127.0.0.1:56370 - "POST /ask HTTP/1.1" 200 OK
INFO:     127.0.0.1:56370 - "POST /ask HTTP/1.1" 429 Too Many Requests
INFO:     127.0.0.1:56370 - "POST /ask HTTP/1.1" 429 Too Many Requests
INFO:     127.0.0.1:56370 - "POST /ask HTTP/1.1" 429 Too Many Requests
INFO:     127.0.0.1:56370 - "POST /ask HTTP/1.1" 429 Too Many Requests
INFO:     127.0.0.1:56370 - "POST /ask HTTP/1.1" 429 Too Many Requests
INFO:     127.0.0.1:56370 - "POST /ask HTTP/1.1" 429 Too Many Requests
INFO:     127.0.0.1:56370 - "POST /ask HTTP/1.1" 429 Too Many Requests
INFO:     127.0.0.1:56370 - "POST /ask HTTP/1.1" 429 Too Many Requests
INFO:     127.0.0.1:56370 - "POST /ask HTTP/1.1" 429 Too Many Requests
INFO:     127.0.0.1:56370 - "POST /ask HTTP/1.1" 429 Too Many Requests
INFO:     127.0.0.1:56370 - "POST /ask HTTP/1.1" 429 Too Many Requests`
- **Dưới ngưỡng giới hạn**: Hoạt động bình thường.
- **Vượt ngưỡng (Request thứ 11/phút)**: `HTTP/1.1 429 Too Many Requests` -> `{"detail": "Rate limit exceeded. Please try again later."}`.

---

### Exercise 4.4: Cost guard
**Logic implement:**
Trong `student_assistant/backend/app/production/cost_guard.py`, hệ thống bảo vệ ngân sách hoạt động như sau:
1. **Track Usage**: mỗi request cộng thêm chi phí cố định `COST_PER_REQUEST_USD` bằng Redis `INCRBYFLOAT`.
2. **Check Budget**: lưu theo key `cost:{user_id}:{YYYY-MM}`; nếu tổng > `MONTHLY_BUDGET_USD` thì trả `402 Payment Required`.
3. **Retention**: key được `EXPIRE` ~90 ngày để dễ debug/đối soát.

---

## Part 5: Scaling & Reliability

### Exercise 5.1: Health checks
1. **Liveness probe (`/health`)**: Được dùng để kiểm tra "Agent có còn sống không?". Nếu endpoint này không phản hồi, platform sẽ tự động restart container để hồi phục dịch vụ. Nó thường chứa thông tin về uptime, version và trạng thái tài nguyên cơ bản.
2. **Readiness probe (`/ready`)**: Được dùng để kiểm tra "Agent đã sẵn sàng nhận traffic chưa?". Load Balancer dựa vào đây để quyết định có gửi yêu cầu vào instance này không. Nó sẽ trả về 503 nếu Agent đang trong quá trình khởi tạo model hoặc đang thực hiện shutdown.

### Exercise 5.2: Graceful shutdown
- **Tại sao quan trọng?**: Ngăn chặn tình trạng mất dữ liệu hoặc lỗi request khi hệ thống thực hiện cập nhật hoặc tự động co giãn (scaling). Thay vì bị "giết" đột ngột, Agent sẽ được thông báo trước để kịp hoàn thành các request đang dang dở.
- **Cách hoạt động**: Khi nhận `SIGTERM`, Uvicorn/FastAPI shutdown và chạy cleanup trong lifespan (đóng Redis connection). Readiness hiện được kiểm tra bằng Redis ping tại `/ready` (không có cờ `ready=false` riêng).

### Exercise 5.3: Stateless design
- **State trong memory (Anti-pattern)**: Khi lưu lịch sử trò chuyện trong RAM của một instance, nếu có nhiều instances chạy song song, người dùng sẽ bị "mất trí nhớ" nếu request tiếp theo của họ được gửi tới một instance khác.
- **Stateless với Redis**: Bằng cách lưu trữ `session` và `history` vào Redis, mọi Agent instance đều có thể truy cập chung một nguồn dữ liệu. Điều này cho phép hệ thống scale ra hàng trăm instance mà vẫn đảm bảo trải nghiệm người dùng nhất quán.

### Exercise 5.4: Load balancing
- **Cơ chế**: Sử dụng Nginx (hoặc Cloud Load Balancer) để phân phối đều requests đến các Agent instances theo thuật toán Round Robin hoặc Least Connections.
- **Lợi ích**: Tăng khả năng chịu tải (high availability) và khả năng mở rộng không giới hạn của hệ thống. Nếu một instance gặp sự cố, Load Balancer sẽ tự động chuyển traffic sang các instances khỏe mạnh còn lại.

---

## Part 6: Final Project (Student Assistant Deployment)

### Implementation Overview
Trong phần này, tôi đã tích hợp các yêu cầu production (Docker multi-stage, env config, auth, rate limit, cost guard, health/readiness, stateless Redis, logging JSON) để triển khai trợ lý sinh viên (`student_assistant`).

### Key Production Features
1. **Stateless Architecture**: 
   - Không lưu state trong RAM của từng instance.
   - Lưu `sessions` trong Redis (`app/auth/sessions.py`) và thread history trong Redis (`app/production/thread_store.py`).
   - Nhờ vậy có thể scale nhiều replica mà không “mất lịch sử”.
2. **Security & Governance**:
   - **Rate Limiting**: Giới hạn 10 requests/phút mỗi người dùng để tránh spam.
   - **Cost Guard**: Kiểm soát ngân sách API LLM, ngăn chặn việc sử dụng quá mức.
   - **API Key Auth**: Chỉ những người dùng/client hợp lệ mới có thể truy cập backend.
3. **Reliability & Scaling**:
   - **Multi-stage Dockerfile**: Giúp image nhỏ gọn (< 300MB), tăng tốc độ deploy.
   - **Nginx Load Balancer**: Điều phối traffic mượt mà giữa các instance.
   - **Health/Readiness Checks**: Platform tự động theo dõi và khôi phục dịch vụ nếu có lỗi.
4. **Observability**:
   - Hệ thống logging cấu trúc JSON giúp dễ dàng theo dõi lỗi và hiệu năng trên các dashboard quản lý tập trung.

### Deployment Information
- **Public URL**: https://lab12-2a202600043-dovietanh.onrender.com
- **Platform**: Render
- **Snapshot**: pics/deploy_part6.png và pics/log_deploy_part6.png
- **Infrastructure**: Docker Compose (Nginx + Backend + Frontend + Redis).
