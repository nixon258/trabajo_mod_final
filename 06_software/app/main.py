"""API del sistema de apoyo a decisiones (DSS)."""
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from . import sim

RAIZ = Path(__file__).resolve().parent
VERSION = "0.1.0"

app = FastAPI(title="DSS Violencia Organizada", version=VERSION,
              description="Simulación de escenarios de contención")


class Peticion(BaseModel):
    modelo: str = Field(default="futuro", description="calibrado | futuro")
    recaudo: float | None = Field(default=None, ge=0, le=200)
    retardo: float | None = Field(default=None, ge=0.5, le=12)
    replicas: int = Field(default=30, ge=1, le=500)


@app.get("/api/salud")
def salud():
    return {"ok": True, "version": VERSION, "modelos": list(sim.MODELOS)}


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


@app.post("/api/simular")
def simular(peticion: Peticion):
    try:
        return sim.simular(peticion.modelo, peticion.recaudo, peticion.retardo,
                           peticion.replicas)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=f"Modelo no encontrado: {exc}") from exc


@app.get("/")
def panel():
    return FileResponse(RAIZ / "static" / "index.html")
