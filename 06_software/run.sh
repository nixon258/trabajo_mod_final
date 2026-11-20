#!/usr/bin/env bash
# Levanta el panel en http://127.0.0.1:8000
set -e
cd "$(dirname "$0")"
if [ -d .venv ]; then
  source .venv/bin/activate
fi
exec uvicorn app.main:app --host 127.0.0.1 --port "${PORT:-8000}" "$@"
