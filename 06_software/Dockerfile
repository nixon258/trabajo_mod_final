# Imagen del DSS. Contexto de construcción: la raíz del repositorio.
#   docker build -f 06_software/Dockerfile -t dss-modelacion .
#   docker run -p 8000:8000 dss-modelacion
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DSS_DB=/datos/dss.db \
    DSS_MAX_CONCURRENT=2

WORKDIR /app
COPY 06_software/requirements.txt 06_software/requirements.txt
RUN pip install --no-cache-dir -r 06_software/requirements.txt

# Código y modelos que consume la API
COPY 06_software/ ./06_software/
COPY 02_informe/modelo_farc.py ./02_informe/
COPY 04_futuro/modelo_futuro.py ./04_futuro/

RUN mkdir -p /datos && useradd -m dss && chown -R dss:dss /datos /app
USER dss

WORKDIR /app/06_software
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=4s --start-period=8s --retries=3 \
  CMD python -c "import urllib.request;urllib.request.urlopen('http://127.0.0.1:8000/api/salud',timeout=3)"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
