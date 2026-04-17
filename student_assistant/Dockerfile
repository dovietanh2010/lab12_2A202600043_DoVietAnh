# Stage 1: builder
FROM python:3.11-slim AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps -r requirements.txt -w /wheels

# Stage 2: runtime
FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

# Phải sửa trong file Dockerfile thành:
COPY student_assistant/requirements.txt .
COPY student_assistant/backend ./backend


EXPOSE 8000
WORKDIR /app/backend
CMD python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
