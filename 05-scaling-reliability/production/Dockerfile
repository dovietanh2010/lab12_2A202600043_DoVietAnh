# Production Dockerfile for Scaling Demo
FROM python:3.11-slim

WORKDIR /app

# Cài đặt dependencies
RUN pip install --no-cache-dir fastapi uvicorn redis psutil

# Copy mã nguồn
COPY . .

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
