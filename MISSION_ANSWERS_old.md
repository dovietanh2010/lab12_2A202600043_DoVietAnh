# Day 12 Lab - Mission Answers (old)

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
1. **Base image là gì?**: image nền chứa sẵn Python 3.11 để build container`python:3.11` (Bản đầy đủ, dung lượng lớn).
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
- **Public URL (Railway)**: https://lab12part3-production.up.railway.app
- **Public URL (Render)**: https://ai-agent-1oa6.onrender.com
- **Platform**: Render (via Blueprint) & Railway (via CLI)
- **Cách thực hiện**:
    *   **Railway**: Dùng Railway CLI (`railway up`) để deploy nhanh từ terminal.
    *   **Render**: Dùng file `render.yaml` (Blueprint) kết nối với GitHub để tự động hóa hạ tầng (IaC).

### Exercise 3.2: Compare config files
- **`railway.toml` vs `render.yaml`**:
    *   **`railway.toml`**: Đơn giản, tập trung vào lệnh chạy (`startCommand`) và cách build. Phù hợp cho các ứng dụng nhỏ, cần deploy nhanh.
    *   **`render.yaml`**: Mạnh mẽ hơn, cho phép định nghĩa nhiều dịch vụ (Web, Redis, DB) cùng lúc. Đây là mô hình **Infrastructure as Code**, giúp quản lý toàn bộ hệ thống chuyên nghiệp và dễ tái sử dụng.

---

## Part 4: API Security

### Exercise 4.1: API Key authentication
1. **API key được check ở đâu?**: Trong hàm `verify_api_key`, được sử dụng như một **FastAPI Dependency**. Nó kiểm tra sự tồn tại và tính hợp lệ của header `X-API-Key`.
2. **Điều gì xảy ra nếu sai key?**: 
    * Nếu thiếu header: Trả về `401 Unauthorized`.
    * Nếu key không khớp: Trả về `403 Forbidden` với thông báo "Invalid API key.".
3. **Làm sao rotate key?**: Chỉ cần thay đổi giá trị của biến môi trường `AGENT_API_KEY` trong file `.env` hoặc trên Dashboard của Cloud Platform (Railway/Render), sau đó restart service.

### Exercise 4.3: Rate limiting
1. **Algorithm nào được dùng?**: **Sliding Window Counter**. Thuật toán này sử dụng một hàng đợi (`deque`) để lưu trữ timestamps của các request trong 60 giây gần nhất, giúp kiểm soát lưu lượng mượt mà hơn Fixed Window.
2. **Limit là bao nhiêu requests/minute?**: 
    * Người dùng thông thường (`user` role): **10 requests/phút**.
    * Quản trị viên (`admin` role): **100 requests/phút**.
3. **Làm sao bypass limit cho admin?**: Admin không bypass hoàn toàn mà được gán một bộ giới hạn riêng (`rate_limiter_admin`) với định mức cao hơn hẳn người dùng thường, giúp họ có thể thực hiện nhiều tác vụ quản trị hơn.

### Exercise 4.4: Cost guard
**Logic implement:**
Lấy cảm hứng từ file `cost_guard.py`, hệ thống bảo vệ ngân sách hoạt động như sau:
1. **Track Usage**: Sau mỗi lần Agent trả lời, hệ thống tính toán chi phí (USD) dựa trên số lượng tokens input/output.
2. **Check Budget**: Trước mỗi request, hệ thống kiểm tra:
    * **Per-user budget**: Mỗi user có hạn mức (ví dụ $1/ngày). Nếu vượt quá, trả về `402 Payment Required`.
    * **Global budget**: Tổng chi phí của toàn hệ thống (ví dụ $10/ngày). Nếu vượt quá, trả về `503 Service Unavailable` để bảo vệ tài chính cho chủ sở hữu Agent.
3. **Reset**: Dữ liệu chi phí được phân tách theo ngày (YYYY-MM-DD) và tự động reset vào lúc nửa đêm.

---

## Part 5: Scaling & Reliability

### Exercise 5.1: Health checks
1. **Liveness probe (`/health`)**: Được dùng để kiểm tra "Agent có còn sống không?". Nếu endpoint này không phản hồi, platform sẽ tự động restart container để hồi phục dịch vụ. Nó thường chứa thông tin về uptime, version và trạng thái tài nguyên cơ bản.
2. **Readiness probe (`/ready`)**: Được dùng để kiểm tra "Agent đã sẵn sàng nhận traffic chưa?". Load Balancer dựa vào đây để quyết định có gửi yêu cầu vào instance này không. Nó sẽ trả về 503 nếu Agent đang trong quá trình khởi tạo model hoặc đang thực hiện shutdown.

### Exercise 5.2: Graceful shutdown
- **Tại sao quan trọng?**: Ngăn chặn tình trạng mất dữ liệu hoặc lỗi request khi hệ thống thực hiện cập nhật hoặc tự động co giãn (scaling). Thay vì bị "giết" đột ngột, Agent sẽ được thông báo trước để kịp hoàn thành các request đang dang dở.
- **Cách hoạt động**: Khi nhận tín hiệu `SIGTERM`, Agent sẽ chuyển sang trạng thái `ready = False` (để Load Balancer ngừng gửi request mới) và sau đó đợi cho toàn bộ các request đang thực thi hoàn tất trước khi chính thức dừng tiến trình.

### Exercise 5.3: Stateless design
- **State trong memory (Anti-pattern)**: Khi lưu lịch sử trò chuyện trong RAM của một instance, nếu có nhiều instances chạy song song, người dùng sẽ bị "mất trí nhớ" nếu request tiếp theo của họ được gửi tới một instance khác.
- **Stateless với Redis**: Bằng cách lưu trữ `session` và `history` vào Redis, mọi Agent instance đều có thể truy cập chung một nguồn dữ liệu. Điều này cho phép hệ thống scale ra hàng trăm instance mà vẫn đảm bảo trải nghiệm người dùng nhất quán.

### Exercise 5.4: Load balancing
- **Cơ chế**: Sử dụng Nginx (hoặc Cloud Load Balancer) để phân phối đều requests đến các Agent instances theo thuật toán Round Robin hoặc Least Connections.
- **Lợi ích**: Tăng khả năng chịu tải (high availability) và khả năng mở rộng không giới hạn của hệ thống. Nếu một instance gặp sự cố, Load Balancer sẽ tự động chuyển traffic sang các instances khỏe mạnh còn lại.

---

## Part 6: Final Project (Student Assistant Deployment)

### Implementation Overview
Trong phần này, tôi đã tích hợp tất cả các kiến thức từ Part 1 đến Part 5 để xây dựng một Production-ready AI Agent cho trợ lý sinh viên (`student_assistant`).

### Key Production Features
1. **Stateless Architecture**: 
   - Sử dụng `RedisSaver` cho LangGraph thay vì `InMemorySaver`.
   - Lưu trữ `sessions` người dùng trong Redis.
   - Điều này cho phép hệ thống mở rộng (scale-out) mà không làm mất lịch sử trò chuyện.
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
- **URL**: [Đang triển khai]
- **Infrastructure**: Docker Compose (Nginx + Backend + Frontend + Redis).
