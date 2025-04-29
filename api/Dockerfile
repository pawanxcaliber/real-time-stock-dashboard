# Stage 1: Build Stage
FROM python:3.12-slim-bullseye as builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ---

# Stage 2: Runtime Stage
FROM python:3.12-slim-bullseye

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

COPY app.py .

RUN adduser --system --group appuser

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["python", "app.py"]