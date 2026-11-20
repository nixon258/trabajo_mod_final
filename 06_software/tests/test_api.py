#!/usr/bin/env python3
"""Pruebas de aceptación del DSS."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from app.main import app
from app import sim

cliente = TestClient(app)


def test_salud():
    r = cliente.get("/api/salud")
    assert r.status_code == 200
    assert r.json()["ok"] is True
    assert "futuro" in r.json()["modelos"]


def test_modelos_expone_los_dos():
    r = cliente.get("/api/modelos")
    datos = r.json()
    assert set(datos) == {"calibrado", "futuro"}
    assert datos["calibrado"]["horizonte"].startswith("84")
    assert datos["futuro"]["horizonte"].startswith("60")


def test_linea_base_futuro_similar_al_modelo():
    """30 réplicas deben acercarse a los 211 atentados del modelo completo."""
    d = cliente.post("/api/simular", json={"modelo": "futuro", "replicas": 10}).json()
    assert 170 <= d["total"] <= 250
    assert d["meses"] == 60
    assert len(d["trayectoria"]) == 60


def test_calibrado_responde():
    d = cliente.post("/api/simular", json={"modelo": "calibrado", "replicas": 10}).json()
    assert d["meses"] == 84
    assert d["total"] > 0


def test_reducir_recaudo_evita_atentados():
    base = cliente.post("/api/simular", json={"modelo": "futuro", "replicas": 10}).json()
    corte = cliente.post("/api/simular",
                         json={"modelo": "futuro", "recaudo": 20, "replicas": 10}).json()
    assert corte["total"] < base["total"]
    assert corte["evitados"] > 0


def test_validacion_de_rangos():
    r = cliente.post("/api/simular", json={"modelo": "futuro", "recaudo": 500})
    assert r.status_code == 422
    r = cliente.post("/api/simular", json={"modelo": "futuro", "retardo": 40})
    assert r.status_code == 422


def test_reproducibilidad():
    a = sim.simular("futuro", recaudo=40, retardo=2, replicas=5)
    b = sim.simular("futuro", recaudo=40, retardo=2, replicas=5)
    assert a["total"] == b["total"]
    assert a["trayectoria"] == b["trayectoria"]


def test_panel_se_sirve():
    r = cliente.get("/")
    assert r.status_code == 200
    assert "Sistema de apoyo a decisiones" in r.text
