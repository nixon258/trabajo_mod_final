#!/usr/bin/env python3
"""
Modelo de simulación de los ciclos de violencia de las FARC (1998-2004).

Dinámica de sistemas con cinco niveles, paso mensual y calibración por
momentos (media, varianza, distribución por categorías y meses sin atentados).
Implementación reproducible en Python; las ecuaciones son trasladables a Vensim.

Uso:
    python modelo_farc.py                # calibración + escenarios + figuras
"""
import argparse
import json
import os

import numpy as np

MESES = 84  # enero de 1998 a diciembre de 2004
REPLICAS = 200

# Parámetros calibrados (búsqueda aleatoria sobre 2.000 combinaciones; ver bitácora)
P = {
    "miedo_inicial": 0.65,
    "mu0": 1.0e5,        # escala de la oportunidad de atentar
    "k": 34.5,           # sensibilidad de la oportunidad a la severidad estatal
    "s0": 0.28,          # umbral de severidad
    "tau": 4.0,          # meses de retardo de la respuesta del Estado
    "dmg": 0.09,         # daño que aporta cada atentado al miedo
    "olvido": 0.38,      # velocidad de olvido del miedo
    "cmd": 0.30,         # comandos por miembro activo
    "compra": 8.0,       # gasto mensual en material
    "mat_use": 3.0,      # material consumido por atentado
    "mat_max": 250.0,    # capacidad de acopio de material
    "rec": 100.0,        # potencial de recaudo mensual
    "cost_h": 0.25,      # sostenimiento por miembro
    "reclut": 0.01,      # reclutamiento por miembro activo
    "bajas": 0.002,      # bajas mensuales
}

INICIAL = {"miedo": 0.65, "economicos": 200.0, "humanos": 150.0,
           "materiales": 200.0, "reclutas": 8.0}

ESCENARIOS = {
    "Línea base": {},
    "Mayor severidad estatal": {"k": 54.0},
    "Financiación reducida 60 %": {"rec": 40.0},
}


def simular(p, semilla=0, meses=MESES):
    """Una réplica del modelo. Devuelve atentados, miedo y material por mes."""
    rng = np.random.default_rng(semilla)
    miedo = severidad = p["miedo_inicial"]
    economicos, humanos = INICIAL["economicos"], INICIAL["humanos"]
    material, reclutas = INICIAL["materiales"], INICIAL["reclutas"]

    atentados, serie_miedo, serie_material = [], [], []

    for _ in range(meses):
        # 1. Oportunidad de atentar: Poisson cuya media cae con la severidad del Estado
        mu = max(1e-4, p["mu0"] * np.exp(-p["k"] * (severidad - p["s0"])))
        oportunidad = rng.poisson(mu)

        # 2. Capacidad operativa: comandos disponibles y material
        comandos = p["cmd"] * humanos
        capacidad = int(min(0.75 * comandos, material / 10.0))
        a = int(min(capacidad, oportunidad))

        atentados.append(a)
        serie_miedo.append(miedo)
        serie_material.append(material)

        # 3. Miedo: entra con el daño, sale con el olvido
        entrada = min(1 - np.exp(-a * p["dmg"]), 1 - miedo)
        miedo = float(np.clip(miedo + entrada - p["olvido"] * miedo, 0, 1))

        # 4. Severidad estatal: sigue al miedo con retardo
        severidad += (miedo - severidad) / p["tau"]

        # 5. Recursos económicos: recaudo proporcional al miedo
        gasto = p["cost_h"] * humanos
        gasto_material = min(p["compra"], max(0.0, economicos))
        economicos = max(0.0, economicos + p["rec"] * (0.3 + miedo) - gasto - gasto_material)

        # 6. Recursos materiales: compras, incautaciones irregulares, uso y depreciación
        irregulares = max(0.0, rng.normal(4, 2))
        material = min(p["mat_max"], max(
            0.0, material + 0.8 * gasto_material + irregulares
            - 0.01 * material - p["mat_use"] * a))

        # 7. Recursos humanos: reclutas en entrenamiento y bajas
        reclutas = reclutas + p["reclut"] * humanos - reclutas
        humanos = max(10.0, humanos + reclutas - p["bajas"] * humanos)

    return (np.array(atentados, dtype=float), np.array(serie_miedo),
            np.array(serie_material), economicos)


def metricas(samples):
    a = np.concatenate(samples)
    return {
        "media": float(a.mean()),
        "varianza": float(a.var()),
        "p_0_3": float((a <= 3).mean()),
        "p_4_10": float(((a >= 4) & (a <= 10)).mean()),
        "p_mas_10": float((a > 10).mean()),
        "meses_sin": float((a == 0).mean() * MESES),
        "maximo": float(a.max()),
        "total": float(a.mean() * MESES),
    }


def correr_escenarios(replicas=REPLICAS):
    resultados = {}
    for nombre, cambios in ESCENARIOS.items():
        p = dict(P, **cambios)
        corridas = [simular(p, semilla=1000 + i) for i in range(replicas)]
        muestras = [c[0] for c in corridas]
        m = metricas(muestras)
        m["miedo_promedio"] = float(np.mean([c[1].mean() for c in corridas]))
        m["material_promedio"] = float(np.mean([c[2].mean() for c in corridas]))
        m["media_por_mes"] = np.mean([c[0] for c in corridas], axis=0).tolist()
        resultados[nombre] = m
    return resultados


REAL = {"media": 3.82, "varianza": 5.43, "p_0_3": 0.71, "p_4_10": 0.19,
        "p_mas_10": 0.10, "meses_sin": 15, "maximo": 25, "total": 3.82 * MESES}


def figura_series(ruta, serie, media_real):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
    fig, ax = plt.subplots(figsize=(6.4, 2.7), dpi=300)
    x = np.arange(1, len(serie) + 1)
    ax.bar(x, serie, color="#1F3864", width=0.75, label="Atentados simulados")
    ax.axhline(media_real, color="#C00000", lw=1.2, ls="--",
               label=f"Media real ({media_real:.2f})")
    ax.set_xlabel("Mes de simulación (1 = enero de 1998)")
    ax.set_ylabel("Atentados por mes")
    ax.set_xlim(0.5, len(serie) + 0.5)
    ax.grid(axis="y", color="#DDDDDD", lw=0.6)
    ax.set_axisbelow(True)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    ax.legend(frameon=False, loc="upper right", fontsize=8)
    fig.tight_layout()
    fig.savefig(ruta)
    plt.close(fig)


def figura_escenarios(ruta, resultados):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
    nombres = list(resultados)
    medias = [resultados[n]["media"] for n in nombres]
    fig, ax = plt.subplots(figsize=(6.4, 2.6), dpi=300)
    colores = ["#1F3864", "#2E75B6", "#A6A6A6"]
    barras = ax.barh(nombres[::-1], medias[::-1], color=colores[:len(nombres)][::-1],
                     height=0.55)
    ax.axvline(REAL["media"], color="#C00000", lw=1.2, ls="--",
               label=f"Media real ({REAL['media']:.2f})")
    ax.legend(frameon=False, loc="lower right", fontsize=8)
    for b, v in zip(barras, medias[::-1]):
        ax.text(v + 0.06, b.get_y() + b.get_height() / 2, f"{v:.2f}",
                va="center", fontsize=8)
    ax.set_xlabel("Atentados promedio por mes")
    ax.set_xlim(0, max(medias + [REAL["media"]]) * 1.2)
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

    resultados = correr_escenarios(args.replicas)
    base = resultados["Línea base"]

    # Una réplica representativa para la figura de series
    serie = simular(P, semilla=2024)[0]
    figura_series(os.path.join(args.salida, "fig_serie.png"), serie, REAL["media"])
    figura_escenarios(os.path.join(args.salida, "fig_escenarios.png"), resultados)

    salida = {
        "parametros": P,
        "inicial": INICIAL,
        "replicas": args.replicas,
        "meses": MESES,
        "real": REAL,
        "escenarios": resultados,
        "validacion": {
            "media": {"real": REAL["media"], "sim": base["media"]},
            "varianza": {"real": REAL["varianza"], "sim": base["varianza"]},
            "p_0_3": {"real": REAL["p_0_3"], "sim": base["p_0_3"]},
            "p_4_10": {"real": REAL["p_4_10"], "sim": base["p_4_10"]},
            "p_mas_10": {"real": REAL["p_mas_10"], "sim": base["p_mas_10"]},
            "meses_sin": {"real": REAL["meses_sin"], "sim": base["meses_sin"]},
        },
    }
    ruta = os.path.join(args.salida, "resultados_modelo.json")
    with open(ruta, "w", encoding="utf-8") as fh:
        json.dump(salida, fh, ensure_ascii=False, indent=1)

    print(json.dumps(salida["validacion"], indent=1, ensure_ascii=False))
    print("escenarios")
    for n, m in resultados.items():
        print(f"  {n}: media={m['media']:.2f} var={m['varianza']:.2f} "
              f"sin={m['meses_sin']:.1f} miedo={m['miedo_promedio']:.3f}")
    print("json ->", ruta)


if __name__ == "__main__":
    main()
