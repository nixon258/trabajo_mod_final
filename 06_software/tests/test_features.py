"""Pruebas de comparación, historial, PDF, ETL y clave de API."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from app.main import app

cliente = TestClient(app)


def _csv_sintetico(meses=36):
    import random
    random.seed(1)
    filas = ["mes,atentados"]
    for i in range(1, meses + 1):
        valor = 0 if i % 7 == 0 else random.randint(1, 8)
        filas.append(f"2020-{i:02d},{valor}")
    return "\n".join(filas).encode()


def test_comparar_tres_escenarios():
    r = cliente.post("/api/comparar", json={
        "modelo": "futuro", "replicas": 5,
        "escenarios": [
            {"nombre": "Base", "recaudo": 100, "retardo": 4},
            {"nombre": "Corte 60", "recaudo": 40, "retardo": 4},
            {"nombre": "Corte 80", "recaudo": 20, "retardo": 2},
        ]})
    assert r.status_code == 200
    datos = r.json()
    assert len(datos["escenarios"]) == 3
    assert all("id" in e for e in datos["escenarios"])
    totales = [e["total"] for e in datos["escenarios"]]
    assert totales[2] < totales[0]


def test_historial_y_detalle():
    cliente.post("/api/simular", json={"modelo": "futuro", "replicas": 5})
    h = cliente.get("/api/historial?limite=5").json()["corridas"]
    assert h and "total" in h[0]
    detalle = cliente.get(f"/api/historial/{h[0]['id']}")
    assert detalle.status_code == 200
    assert detalle.json()["resultado"]["modelo"] == "futuro"


def test_pdf_de_una_corrida():
    r = cliente.post("/api/simular", json={"modelo": "calibrado", "replicas": 5})
    corrida_id = r.json()["id"]
    pdf = cliente.get(f"/api/historial/{corrida_id}/pdf")
    assert pdf.status_code == 200
    assert pdf.headers["content-type"] == "application/pdf"
    assert pdf.content[:4] == b"%PDF"


def test_historial_inexistente():
    assert cliente.get("/api/historial/999999").status_code == 404


def test_etl_csv_valido():
    r = cliente.post("/api/datos/validar",
                     files={"archivo": ("serie.csv", _csv_sintetico(), "text/csv")})
    assert r.status_code == 200
    d = r.json()
    assert d["meses"] == 36
    assert "referencia" in d


def test_etl_rechaza_columnas_invalidas():
    r = cliente.post("/api/datos/validar",
                     files={"archivo": ("serie.csv", b"a,b\n1,2\n", "text/csv")})
    assert r.status_code == 422


def test_clave_de_api(monkeypatch):
    import app.main as main
    monkeypatch.setattr(main, "API_KEY", "secreta")
    sin = cliente.post("/api/simular", json={"modelo": "futuro", "replicas": 2})
    assert sin.status_code == 401
    con = cliente.post("/api/simular", json={"modelo": "futuro", "replicas": 2},
                       headers={"X-API-Key": "secreta"})
    assert con.status_code == 200


def test_limites_declarados():
    d = cliente.get("/api/limites").json()
    assert "no_es_pronostico" in d and "geografia" in d
