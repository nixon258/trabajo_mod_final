# Riesgos del DSS y su mitigación

Estado al cierre del incremento 2. Cada riesgo tiene una medida aplicada y una evidencia
verificable en el repositorio.

| # | Riesgo | Prob. / impacto | Mitigación aplicada | Evidencia | Residual |
|---|---|---|---|---|---|
| 1 | JaamSim exige Java 17+ y el servidor tiene 11 | Alta / alto | El DSS **no invoca JaamSim**: consume los modelos en Python. JaamSim queda como módulo de verificación aparte, con comando documentado y Java 21 explícito | `06_software/app/sim.py`, `03_exposicion/demo_jaamsim.md` | La demo en vivo sigue necesitando JDK 21 en el equipo |
| 2 | Parseo de `.dat` y locale decimal | Media / alto | No se parsea `.dat`. La API devuelve JSON numérico; el panel formatea a es-CO solo en pantalla; el CSV usa punto decimal | `tests/test_features.py`, `app/sim.py` | — |
| 3 | Saturación por concurrencia y latencia | Media / alto | Semáforo configurable (`DSS_MAX_CONCURRENT`), ejecución en hilo aparte, caché de línea base, 503 explícito al saturarse | `app/main.py`, `scripts/smoke.sh` | Una petición por worker; escalar con procesos o contenedores |
| 4 | El panel promete más de lo que el modelo puede decir | Media / alto | Bloque fijo de advertencia en el panel, endpoint `/api/limites`, PDF con advertencia de alcance | `app/static/index.html`, `app/report.py`, `tests/test_features.py::test_limites_declarados` | Comunicación: depende de cómo se lea en la exposición |
| 5 | Datos sensibles en el prototipo | Media / alto | No hay ingesta externa: el ETL valida CSV que sube el usuario. Sin datos de inteligencia financiera | `app/etl.py` | Un despliegue público requiere HTTPS y política de datos |
| 6 | Pérdida de historial | Media / medio | SQLite en modo WAL, volumen Docker `/datos`, ruta configurable por `DSS_DB` | `app/db.py`, `docker-compose.yml` | Sin respaldo automático programado |
| 7 | Entradas inválidas rompen la corrida | Alta / medio | Validación Pydantic con rangos (recaudo 0–200, retardo 0,5–12, réplicas 1–500) y 422 con mensaje | `tests/test_api.py::test_validacion_de_rangos` | — |
| 8 | Acceso no autorizado en despliegue | Media / medio | Clave opcional por `DSS_API_KEY` (header `X-API-Key`); abierta solo en local | `app/main.py`, `tests/test_features.py::test_clave_de_api` | Sin roles ni usuarios: es una clave compartida |
| 9 | Dependencias cambian y rompen el build | Media / medio | `requirements.txt` con mínimos; Docker fija `python:3.12-slim` | `requirements.txt`, `Dockerfile` | Sin archivo de bloqueo (`pip freeze`) |
| 10 | Archivos que no deben versionarse | Alta / bajo | `.gitignore` cubre `dss.db*`, `__pycache__`, `.venv` | `.gitignore` | — |
| 11 | Interpretar la proyección como pronóstico | Media / alto | Advertencia en panel, PDF, README y `/api/limites`; el modelo proyecta el mecanismo, no a las FARC | `README.md`, `04_futuro/proyeccion_2031.pdf` | Riesgo de comunicación, no de código |
| 12 | Sin validación fuera de muestra | Alta / alto | Declarado como límite; el ETL permite cargar una serie nueva para recalibrar | `/api/limites`, `app/etl.py` | Requiere datos posteriores a 2004 |

## Riesgos que no se pueden cerrar en este incremento

1. **Validación externa del modelo**: no hay serie posterior a 2004 en el repositorio. El ETL
   queda listo, pero la recalibración es trabajo de la siguiente fase.
2. **Autenticación multiusuario**: una clave compartida no reemplaza usuarios y roles.
3. **Cola de tareas distribuida**: el semáforo protege un proceso; para varias réplicas
   concurrentes hace falta Celery/RabbitMQ o varios contenedores detrás de un proxy.
4. **Build de Docker**: el daemon no está disponible en esta máquina, así que la imagen no se
   construyó. El Dockerfile se revisó a mano y el humo se validó sin contenedor.

## Cómo verificar las mitigaciones

```bash
cd 06_software
python -m pytest tests -q          # 16 pruebas
./scripts/smoke.sh                 # salud, simulación, PDF y límites
```

Resultado esperado: 16 pruebas en verde y `SMOKE OK`.
