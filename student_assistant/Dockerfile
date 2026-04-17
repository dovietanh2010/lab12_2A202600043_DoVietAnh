# Stage 1: Build Frontend (Next.js)
FROM node:18-alpine AS frontend-builder
WORKDIR /build-frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Build Backend Wheels
FROM python:3.11-slim AS backend-builder
WORKDIR /build-backend
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps -r requirements.txt -w /wheels

# Stage 3: Runtime
FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies from wheels
COPY --from=backend-builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

# Copy backend code
COPY student_assistant/requirements.txt .
COPY student_assistant/backend ./backend

# Copy built frontend to backend/static
COPY --from=frontend-builder /build-frontend/out ./backend/static

EXPOSE 8000
WORKDIR /app/backend
CMD python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
