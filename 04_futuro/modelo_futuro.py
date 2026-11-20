#!/usr/bin/env python3
"""
Proyección exploratoria del mecanismo de violencia organizada, 2027-2031.

No pronostica hechos: extiende la estructura calibrada con la serie 1998-2004
para comparar escenarios de política en un horizonte de 60 meses.

Uso:
    python modelo_futuro.py [--replicas 200]
"""
import argparse
import json
import os

import numpy as np

MESES = 60  # enero 2027 - diciembre 2031
REPLICAS = 200
ANIO_INICIO = 2027

P = {
    "mu0": 1.0e5,
    "k": 34.5,
    "s0": 0.28,
    "tau": 4.0,
    "dmg": 0.09,
    "olvido": 0.38,
    "cmd": 0.30,
    "compra": 8.0,
    "mat_use": 3.0,
    "mat_max": 250.0,
    "rec": 100.0,
    "cost_h": 0.25,
    "reclut": 0.01,
    "bajas": 0.002,
    "anticipacion": 0.0,   # 0 = responde al nivel de miedo; >0 = responde a la tendencia
}

# Supuestos de arranque para 2027 (declarados en el informe)
INICIAL = {"miedo": 0.58, "economicos": 200.0, "humanos": 150.0,
           "materiales": 200.0, "reclutas": 5.0}

ESCENARIOS = {
    "Tendencial": {},
    "Financiamiento -60 %": {"rec": 40.0},
    "Paquete institucional": {"rec": 40.0, "k": 54.0, "tau": 2.0},
    "Financiamiento -80 %": {"rec": 20.0},
}


CALENTAMIENTO = 3  # meses descartados para eliminar el transitorio inicial


def simular(p, semilla=0, meses=MESES):
    rng = np.random.default_rng(semilla)
    total = meses + CALENTAMIENTO
    miedo = severidad = INICIAL["miedo"]
    economicos, humanos = INICIAL["economicos"], INICIAL["humanos"]
    material, reclutas = INICIAL["materiales"], INICIAL["reclutas"]

    atentados, serie_miedo = [], []
    miedo_prev = miedo

    for _ in range(total):
        mu = max(1e-3, p["mu0"] * np.exp(-p["k"] * (severidad - p["s0"])))
        oportunidad = rng.poisson(mu)

        comandos = p["cmd"] * humanos
        capacidad = int(min(0.75 * comandos, material / 10.0))
        a = int(min(capacidad, oportunidad))

        atentados.append(a)
        serie_miedo.append(miedo)

        entrada = min(1 - np.exp(-a * p["dmg"]), 1 - miedo)
        miedo = float(np.clip(miedo + entrada - p["olvido"] * miedo, 0, 1))

        # Anticipación: la respuesta reacciona a la tendencia, no solo al nivel
        tendencia = max(0.0, miedo - miedo_prev)
        objetivo = np.clip(miedo + p["anticipacion"] * tendencia, 0, 1)
        severidad += (objetivo - severidad) / p["tau"]
        miedo_prev = miedo

        gasto = p["cost_h"] * humanos
        gasto_material = min(p["compra"], max(0.0, economicos))
        economicos = max(0.0, economicos + p["rec"] * (0.3 + miedo)
                         - gasto - gasto_material)

        irregulares = max(0.0, rng.normal(4, 2))
        material = min(p["mat_max"], max(
            0.0, material + 0.8 * gasto_material + irregulares
            - 0.01 * material - p["mat_use"] * a))

        reclutas = reclutas + p["reclut"] * humanos - reclutas
        humanos = max(10.0, humanos + reclutas - p["bajas"] * humanos)

    return (np.array(atentados[CALENTAMIENTO:], dtype=float),
            np.array(serie_miedo[CALENTAMIENTO:]), np.array([material]))


def metricas(corridas):
    a = np.concatenate([c[0] for c in corridas])
    totales = np.array([c[0].sum() for c in corridas])
    return {
        "media_mensual": float(a.mean()),
        "varianza": float(a.var()),
        "total_5_anios": float(totales.mean()),
        "meses_sin_atentados": float((a == 0).mean() * MESES),
        "p_mas_10": float((a > 10).mean()),
        "miedo_promedio": float(np.mean([c[1].mean() for c in corridas])),
        "total_ic95": float(1.96 * totales.std(ddof=1) / np.sqrt(len(totales))),
    }


def correr(replicas=REPLICAS):
    resultados = {}
    totales_por_semilla = {}
    for nombre, cambios in ESCENARIOS.items():
        p = dict(P, **cambios)
        corridas = [simular(p, semilla=5000 + i) for i in range(replicas)]
        m = metricas(corridas)
        m["trayectoria"] = np.mean([c[0] for c in corridas], axis=0).tolist()
        resultados[nombre] = m
        totales_por_semilla[nombre] = np.array([c[0].sum() for c in corridas])

    base = totales_por_semilla["Tendencial"]
    for nombre in resultados:
        evitados = base - totales_por_semilla[nombre]
        resultados[nombre]["evitados"] = float(evitados.mean())
        resultados[nombre]["evitados_pct"] = float((evitados / base).mean() * 100)
    return resultados


def figura_trayectorias(ruta, resultados):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
    fig, ax = plt.subplots(figsize=(7.2, 3.4), dpi=300)
    estilos = [("#7F7F7F", "--"), ("#2E75B6", "-"), ("#1F3864", "-"), ("#C00000", "-")]
    x = np.arange(1, MESES + 1)
    for (nombre, m), (color, ls) in zip(resultados.items(), estilos):
        ax.plot(x, m["trayectoria"], color=color, ls=ls, lw=1.6, label=nombre)
    ax.set_xlabel("Mes de la proyección (1 = enero de 2027)")
    ax.set_ylabel("Atentados por mes (promedio de 200 réplicas)")
    ax.set_xlim(1, MESES)
    ax.grid(axis="y", color="#DDDDDD", lw=0.6)
    ax.set_axisbelow(True)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    ax.legend(frameon=False, fontsize=7.5, loc="upper right")
    fig.tight_layout()
    fig.savefig(ruta)
    plt.close(fig)


def figura_evitados(ruta, resultados):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
    nombres = [n for n in resultados if n != "Tendencial"]
    evitados = [resultados[n]["evitados"] for n in nombres]
    fig, ax = plt.subplots(figsize=(7.2, 2.8), dpi=300)
    barras = ax.barh(nombres[::-1], evitados[::-1], color=["#C00000", "#1F3864", "#2E75B6"],
                     height=0.55)
    base = resultados["Tendencial"]["total_5_anios"]
    for b, v in zip(barras, evitados[::-1]):
        ax.text(v + base * 0.01, b.get_y() + b.get_height() / 2,
                f"{v:.0f} ({v / base * 100:.0f} %)", va="center", fontsize=8)
    ax.set_xlabel(f"Atentados evitados en 60 meses (base tendencial: {base:.0f})")
    ax.set_xlim(0, max(evitados) * 1.28)
    ax.grid(axis="x", color="#DDDDDD", lw=0.6)
    ax.set_axisbelow(True)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    fig.tight_layout()
    fig.savefig(ruta)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--replicas", type=int, default=REPLICAS)
    ap.add_argument("--salida", default=os.path.dirname(os.path.abspath(__file__)))
    args = ap.parse_args()

    resultados = correr(args.replicas)
    figura_trayectorias(os.path.join(args.salida, "fig_trayectorias.png"), resultados)
    figura_evitados(os.path.join(args.salida, "fig_evitados.png"), resultados)

    salida = {"parametros": P, "inicial": INICIAL, "meses": MESES,
              "anio_inicio": ANIO_INICIO, "replicas": args.replicas,
              "escenarios": resultados}
    ruta = os.path.join(args.salida, "resultados_futuro.json")
    with open(ruta, "w", encoding="utf-8") as fh:
        json.dump(salida, fh, ensure_ascii=False, indent=1)

    print(f"{'Escenario':38s} {'media':>6s} {'total':>7s} {'evitados':>9s} {'%':>6s} "
          f"{'sin':>5s} {'>10':>5s} {'miedo':>6s}")
    for nombre, m in resultados.items():
        print(f"{nombre:38s} {m['media_mensual']:6.2f} {m['total_5_anios']:7.0f} "
              f"{m['evitados']:9.0f} {m['evitados_pct']:5.1f}% "
              f"{m['meses_sin_atentados']:5.1f} {m['p_mas_10'] * 100:4.0f}% "
              f"{m['miedo_promedio']:6.2f}")
    print("json ->", ruta)


if __name__ == "__main__":
    main()
