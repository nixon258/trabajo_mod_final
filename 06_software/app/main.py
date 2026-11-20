"""API del sistema de apoyo a decisiones (DSS)."""
import os
import threading
from pathlib import Path

from fastapi import Depends, FastAPI, File, Header, HTTPException, UploadFile
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import FileResponse, Response
from pydantic import BaseModel, Field

from . import db, etl, report, sim

RAIZ = Path(__file__).resolve().parent
VERSION = "0.2.0"
API_KEY = os.environ.get("DSS_API_KEY", "")
MAX_CONCURRENTES = int(os.environ.get("DSS_MAX_CONCURRENT", "2"))
SEMAFORO = threading.Semaphore(MAX_CONCURRENTES)

LIMITES = {
    "no_es_pronostico": "El modelo compara escenarios bajo una estructura calibrada; no predice hechos.",
    "datos": "Calibrado con la serie 1998-2004. Las FARC se desmovilizaron en 2016.",
    "geografia": "Escala nacional y mensual; no distingue departamentos ni municipios.",
    "incertidumbre": "El intervalo reportado mide ruido de semilla, no error estructural.",
    "costos": "No hay función de costos: no calcula costo-beneficio.",
    "validez_externa": "Sin validación fuera de muestra ni datos posteriores a 2004.",
}

app = FastAPI(title="DSS Violencia Organizada", version=VERSION,
              description="Simulación de escenarios de contención")


db.iniciar()


def requiere_clave(x_api_key: str | None = Header(default=None)):
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Clave de API inválida")


class Peticion(BaseModel):
    modelo: str = Field(default="futuro", description="calibrado | futuro")
    recaudo: float | None = Field(default=None, ge=0, le=200)
    retardo: float | None = Field(default=None, ge=0.5, le=12)
    replicas: int = Field(default=30, ge=1, le=500)
    guardar: bool = Field(default=True, description="Guardar la corrida en el historial")


class Escenario(BaseModel):
    nombre: str = Field(min_length=1, max_length=60)
    recaudo: float = Field(ge=0, le=200)
    retardo: float = Field(ge=0.5, le=12)


class PeticionComparar(BaseModel):
    modelo: str = "futuro"
    escenarios: list[Escenario] = Field(min_length=2, max_length=5)
    replicas: int = Field(default=30, ge=1, le=200)


def _ejecutar(fn, *args):
    if not SEMAFORO.acquire(timeout=30):
        raise HTTPException(status_code=503, detail="Servidor ocupado, intente de nuevo")
    try:
        return run_in_threadpool(fn, *args)
    finally:
        SEMAFORO.release()


@app.get("/api/salud")
def salud():
    return {"ok": True, "version": VERSION, "modelos": list(sim.MODELOS),
            "max_concurrentes": MAX_CONCURRENTES, "clave_requerida": bool(API_KEY)}


@app.get("/api/modelos")
def modelos():
    salida = {}
    for clave, meta in sim.MODELOS.items():
        mod = sim._modulo(clave)
        salida[clave] = {
            "etiqueta": meta["etiqueta"],
            "horizonte": meta["horizonte"],
            "recaudo_base": mod.P["rec"],
            "retardo_base": mod.P["tau"],
        }
    return salida


@app.get("/api/limites")
def limites():
    return LIMITES


@app.post("/api/simular", dependencies=[Depends(requiere_clave)])
async def simular(peticion: Peticion):
    try:
        resultado = await _ejecutar(sim.simular, peticion.modelo, peticion.recaudo,
                                    peticion.retardo, peticion.replicas)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=f"Modelo no encontrado: {exc}") from exc
    if peticion.guardar:
        resultado["id"] = db.guardar(resultado)
    return resultado


@app.post("/api/comparar", dependencies=[Depends(requiere_clave)])
async def comparar(peticion: PeticionComparar):
    resultados = []
    for esc in peticion.escenarios:
        try:
            r = await _ejecutar(sim.simular, peticion.modelo, esc.recaudo, esc.retardo,
                                peticion.replicas)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        r["nombre"] = esc.nombre
        r["id"] = db.guardar(r)
        resultados.append(r)
    return {"modelo": peticion.modelo, "replicas": peticion.replicas,
            "escenarios": resultados}


@app.get("/api/historial", dependencies=[Depends(requiere_clave)])
def historial(limite: int = 20):
    return {"corridas": db.historial(max(1, min(limite, 200)))}


@app.get("/api/historial/{corrida_id}", dependencies=[Depends(requiere_clave)])
def corrida(corrida_id: int):
    datos = db.obtener(corrida_id)
    if datos is None:
        raise HTTPException(status_code=404, detail="Corrida no encontrada")
    return datos


@app.get("/api/historial/{corrida_id}/pdf", dependencies=[Depends(requiere_clave)])
def pdf(corrida_id: int):
    datos = db.obtener(corrida_id)
    if datos is None:
        raise HTTPException(status_code=404, detail="Corrida no encontrada")
    contenido = report.generar(datos["resultado"])
    return Response(contenido, media_type="application/pdf",
                    headers={"Content-Disposition":
                             f'attachment; filename="escenario_{corrida_id}.pdf"'})


@app.post("/api/datos/validar", dependencies=[Depends(requiere_clave)])
async def validar_datos(archivo: UploadFile = File(...)):
    if archivo.size and archivo.size > 2_000_000:
        raise HTTPException(status_code=413, detail="El archivo supera 2 MB")
    contenido = await archivo.read()
    try:
        return etl.validar_csv(contenido)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.get("/")
def panel():
    return FileResponse(RAIZ / "static" / "index.html")
