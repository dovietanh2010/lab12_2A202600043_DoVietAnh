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
1. **Base image là gì?**: `python:3.11` (Bản đầy đủ, dung lượng lớn).
2. **Working directory là gì?**: `/app` (Thư mục làm việc chính bên trong container).
3. **Tại sao COPY requirements.txt trước?**: Để tận dụng **Docker Layer Caching**. Nếu file requirements không đổi, Docker sẽ dùng lại layer đã cài đặt dependencies, giúp build nhanh hơn rất nhiều ở các lần sau.
4. **CMD vs ENTRYPOINT khác nhau thế nào?**:
    *   `CMD`: Thiết lập lệnh mặc định, có thể dễ dàng bị ghi đè khi chạy lệnh `docker run`.
    *   `ENTRYPOINT`: Thiết lập lệnh chính sẽ chạy, khó bị ghi đè hơn và thường được dùng để biến container thành một file thực thi. Ở đây dùng `CMD` để linh hoạt hơn.

### Exercise 2.3: Image size comparison
- Develop: 1.66 GB
- Production: ~165 MB
- Difference: Giảm ~90%

### Exercise 2.4: Docker Compose questions
1. **Services nào được start?**: Agent, Redis và Nginx.
2. **Chúng communicate thế nào?**: Thông qua mạng nội bộ của Docker (Docker bridge network). Nginx đóng vai trò là cổng vào (Reverse Proxy), điều hướng yêu cầu đến Agent. Agent kết nối với Redis để lưu trữ dữ liệu.

### Discussion Questions
1. **Tại sao COPY requirements.txt trước?**: Để tận dụng cache. Nếu code thay đổi nhưng thư viện không đổi, Docker sẽ không phải cài lại thư viện, giúp tiết kiệm thời gian build.
2. **.dockerignore nên chứa những gì?**: Các file không cần thiết như `__pycache__`, `.git`, `venv`, và đặc biệt là file bí mật `.env`. Việc này giúp image nhẹ hơn và an toàn hơn.
3. **Làm sao mount volume?**: Sử dụng flag `-v` khi chạy lệnh `docker run` hoặc khai báo `volumes` trong file `docker-compose.yml`.

---
