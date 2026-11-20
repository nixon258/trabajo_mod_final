#!/usr/bin/env bash
# Prueba de humo sin Docker: levanta la API, consulta los endpoints y la apaga.
set -euo pipefail
cd "$(dirname "$0")/.."

PORT="${PORT:-8099}"
PY="${PY:-python3}"
[ -x .venv/bin/python ] && PY=.venv/bin/python

$PY -m uvicorn app.main:app --host 127.0.0.1 --port "$PORT" >/tmp/dss_smoke.log 2>&1 &
PID=$!
trap 'kill $PID 2>/dev/null || true' EXIT

for _ in $(seq 1 30); do
  curl -sf "http://127.0.0.1:$PORT/api/salud" >/dev/null && break
  sleep 1
done

echo "1/4 salud"
curl -sf "http://127.0.0.1:$PORT/api/salud" | $PY -c "import json,sys; d=json.load(sys.stdin); assert d['ok']; print('   ok', d['version'])"

echo "2/4 simulación"
ID=$(curl -sf -X POST "http://127.0.0.1:$PORT/api/simular" -H 'Content-Type: application/json' \
  -d '{"modelo":"futuro","recaudo":40,"retardo":2,"replicas":10}' \
  | $PY -c "import json,sys; d=json.load(sys.stdin); assert d['total']>0; print(d['id'])")
echo "   corrida $ID"

echo "3/4 pdf"
curl -sf "http://127.0.0.1:$PORT/api/historial/$ID/pdf" -o /tmp/dss_smoke.pdf
head -c 4 /tmp/dss_smoke.pdf | grep -q '%PDF' && echo "   ok"

echo "4/4 límites"
curl -sf "http://127.0.0.1:$PORT/api/limites" | $PY -c "import json,sys; d=json.load(sys.stdin); assert 'no_es_pronostico' in d; print('   ok')"

echo "SMOKE OK"
