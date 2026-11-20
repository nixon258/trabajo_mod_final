"""Capa de simulación: envuelve los dos modelos del proyecto.

Modelo 'calibrado'  -> 02_informe/modelo_farc.py   (1998-2004, 84 meses)
Modelo 'futuro'     -> 04_futuro/modelo_futuro.py  (2027-2031, 60 meses)
"""
import importlib.util
import math
from functools import lru_cache
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]

MODELOS = {
    "calibrado": {
        "ruta": RAIZ / "02_informe" / "modelo_farc.py",
        "etiqueta": "Calibrado 1998-2004",
        "horizonte": "84 meses (1998-2004)",
    },
    "futuro": {
        "ruta": RAIZ / "04_futuro" / "modelo_futuro.py",
        "etiqueta": "Proyección 2027-2031",
        "horizonte": "60 meses (2027-2031)",
    },
}

MODULOS = {}


def _modulo(nombre):
    if nombre not in MODELOS:
        raise ValueError(f"Modelo desconocido: {nombre}. Use {list(MODELOS)}")
    if nombre not in MODULOS:
        spec = importlib.util.spec_from_file_location(f"modelo_{nombre}",
                                                      MODELOS[nombre]["ruta"])
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        MODULOS[nombre] = mod
    return MODULOS[nombre]


def _simular(mod, params, semilla):
    """Adapta la firma de cada modelo (3 o 4 valores de retorno)."""
    salida = mod.simular(params, semilla=semilla)
    return salida[0]


def _validar(recaudo, retardo, replicas):
    if not (0 <= recaudo <= 200):
        raise ValueError("recaudo debe estar entre 0 y 200")
    if not (0.5 <= retardo <= 12):
        raise ValueError("retardo debe estar entre 0.5 y 12 meses")
    if not (1 <= replicas <= 500):
        raise ValueError("replicas debe estar entre 1 y 500")


def _metricas(corridas):
    """Métricas agrupadas sobre las observaciones de todas las réplicas."""
    n = len(corridas)
    meses = len(corridas[0])
    totales = [sum(c) for c in corridas]
    plano = [v for c in corridas for v in c]
    total = sum(totales) / n
    media = sum(plano) / len(plano)
    var_obs = sum((v - media) ** 2 for v in plano) / (len(plano) - 1)
    var_totales = (sum((t - total) ** 2 for t in totales) / (n - 1)) if n > 1 else 0.0
    sin = sum(1 for v in plano if v == 0) / len(plano) * meses
    p10 = sum(1 for v in plano if v > 10) / len(plano) * 100
    trayectoria = [sum(c[i] for c in corridas) / n for i in range(meses)]
    return {
        "total": round(total, 1),
        "media_mensual": round(media, 2),
        "varianza_mensual": round(var_obs, 2),
        "ic95": round(1.96 * math.sqrt(var_totales / n), 1) if n > 1 else 0.0,
        "meses_sin_atentados": round(sin, 1),
        "p_mas_10": round(p10, 1),
        "trayectoria": [round(v, 2) for v in trayectoria],
    }


@lru_cache(maxsize=16)
def _linea_base(nombre, replicas):
    mod = _modulo(nombre)
    corridas = [_simular(mod, dict(mod.P), 9000 + i) for i in range(replicas)]
    return tuple(round(c.sum(), 1) for c in corridas)


def simular(nombre, recaudo=None, retardo=None, replicas=30):
    """Ejecuta un escenario y lo compara con la línea base del mismo modelo."""
    mod = _modulo(nombre)
    p = dict(mod.P)
    if recaudo is not None:
        p["rec"] = float(recaudo)
    if retardo is not None:
        p["tau"] = float(retardo)
    _validar(p["rec"], p["tau"], replicas)

    semillas = [9000 + i for i in range(replicas)]
    corridas = [_simular(mod, p, s) for s in semillas]
    m = _metricas(corridas)

    base = _linea_base(nombre, replicas)
    totales = [c.sum() for c in corridas]
    evitados = [b - t for b, t in zip(base, totales)]
    m["evitados"] = round(sum(evitados) / replicas, 1)
    m["evitados_pct"] = round(sum(evitados) / sum(base) * 100, 1) if sum(base) else 0.0

    m.update({
        "modelo": nombre,
        "etiqueta": MODELOS[nombre]["etiqueta"],
        "horizonte": MODELOS[nombre]["horizonte"],
        "parametros": {"recaudo": p["rec"], "retardo": p["tau"],
                       "replicas": replicas, "semilla_inicial": semillas[0]},
        "meses": len(m["trayectoria"]),
    })
    return m
