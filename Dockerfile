# python:3.9 reached end-of-life in October 2025 — stay on a supported runtime.
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run as an unprivileged user; nothing here needs root.
RUN useradd --create-home --uid 1000 appuser
USER appuser

# No --reload in the image: dev hot-reload belongs in docker-compose only.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
