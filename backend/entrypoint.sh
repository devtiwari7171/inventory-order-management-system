#!/usr/bin/env bash
# Wait for Postgres, run migrations, then start the API server.
set -euo pipefail

# Wait for database to be reachable (max ~60s)
echo "Waiting for database..."
python <<'PY'
import os, time, socket
host = os.getenv("POSTGRES_HOST", "postgres")
port = int(os.getenv("POSTGRES_PORT", "5432"))
deadline = time.time() + 60
while time.time() < deadline:
    try:
        with socket.create_connection((host, port), timeout=2):
            print("Database reachable.")
            break
    except OSError:
        time.sleep(1)
else:
    raise SystemExit("Database not reachable after 60s")
PY

echo "Running migrations..."
alembic upgrade head

echo "Starting API on 0.0.0.0:8000..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2
