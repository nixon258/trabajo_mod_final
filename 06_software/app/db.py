"""Persistencia local de corridas (SQLite)."""
import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

RUTA = Path(os.environ.get("DSS_DB", Path(__file__).resolve().parents[1] / "dss.db"))

ESQUEMA = """
CREATE TABLE IF NOT EXISTS corridas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    creada TEXT NOT NULL,
    modelo TEXT NOT NULL,
    recaudo REAL,
    retardo REAL,
    replicas INTEGER NOT NULL,
    total REAL NOT NULL,
    evitados REAL,
    evitados_pct REAL,
    resultado TEXT NOT NULL
);
"""


def _conexion():
    con = sqlite3.connect(RUTA, timeout=10)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA journal_mode=WAL")
    return con


def iniciar():
    with _conexion() as con:
        con.executescript(ESQUEMA)


def guardar(resultado):
    with _conexion() as con:
        cur = con.execute(
            "INSERT INTO corridas (creada, modelo, recaudo, retardo, replicas, total,"
            " evitados, evitados_pct, resultado) VALUES (?,?,?,?,?,?,?,?,?)",
            (datetime.now(timezone.utc).isoformat(timespec="seconds"),
             resultado["modelo"], resultado["parametros"]["recaudo"],
             resultado["parametros"]["retardo"], resultado["parametros"]["replicas"],
             resultado["total"], resultado["evitados"], resultado["evitados_pct"],
             json.dumps(resultado, ensure_ascii=False)))
        return cur.lastrowid


def historial(limite=20):
    with _conexion() as con:
        filas = con.execute(
            "SELECT id, creada, modelo, recaudo, retardo, replicas, total, evitados_pct"
            " FROM corridas ORDER BY id DESC LIMIT ?", (int(limite),)).fetchall()
    return [dict(f) for f in filas]


def obtener(corrida_id):
    with _conexion() as con:
        fila = con.execute("SELECT * FROM corridas WHERE id = ?", (int(corrida_id),)).fetchone()
    if fila is None:
        return None
    datos = dict(fila)
    datos["resultado"] = json.loads(datos["resultado"])
    return datos
