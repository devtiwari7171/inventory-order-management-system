#!/usr/bin/env bash
# Wait for the database to be reachable, run migrations, then start uvicorn.
# Works in both Docker Compose (POSTGRES_HOST=postgres) and Render/Neon (DATABASE_URL).
set -euo pipefail

echo "Waiting for database to become reachable..."

python <<'PY'
import os, time, socket
from urllib.parse import urlparse

# Prefer DATABASE_URL (used on Render / Neon / production).
# Fall back to POSTGRES_HOST/PORT (used in docker-compose).
db_url = os.getenv("DATABASE_URL")
if db_url:
    parsed = urlparse(db_url)
    host = parsed.hostname
    port = parsed.port or 5432
else:
    host = os.getenv("POSTGRES_HOST", "postgres")
    port = int(os.getenv("POSTGRES_PORT", "5432"))

if not host:
    raise SystemExit("Could not determine database host from DATABASE_URL or POSTGRES_HOST")

print(f"Waiting for database at {host}:{port}...")
deadline = time.time() + 90
attempt = 0
while time.time() < deadline:
    attempt += 1
    try:
        with socket.create_connection((host, port), timeout=3):
            print(f"Database reachable after {attempt} attempt(s).")
            break
    except OSError as e:
        if attempt % 10 == 0:
            print(f"   ...still waiting ({attempt * 2}s elapsed): {e.__class__.__name__}")
        time.sleep(2)
else:
    raise SystemExit(f"Database at {host}:{port} not reachable after 90s")
PY

echo ""
echo "Running database migrations..."
alembic upgrade head

echo ""
echo "Starting API server on 0.0.0.0:8000..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2
