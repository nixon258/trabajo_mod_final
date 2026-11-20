"""Reporte PDF de una corrida, generado con matplotlib (sin dependencias extra)."""
import io

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def _fmt(x, dec=1):
    return f"{x:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def generar(resultado):
    """Devuelve bytes de un PDF de una página."""
    serie = resultado["trayectoria"]
    params = resultado["parametros"]

    fig = plt.figure(figsize=(8.27, 11.69))  # A4 vertical, pulgadas
    fig.patch.set_facecolor("white")

    fig.text(0.09, 0.945, "Sistema de apoyo a decisiones", fontsize=9, color="#595959")
    fig.text(0.09, 0.905, "Reporte de escenario simulado", fontsize=18,
             color="#1F3864", weight="bold")
    fig.text(0.09, 0.877, f"{resultado['etiqueta']} · {resultado['horizonte']}",
             fontsize=10.5, color="#2E75B6")

    lineas = [
        ("Atentados en el horizonte", _fmt(resultado["total"], 1)),
        ("Media mensual", _fmt(resultado["media_mensual"], 2)),
        ("Varianza mensual", _fmt(resultado["varianza_mensual"], 2)),
        ("Meses sin atentados", _fmt(resultado["meses_sin_atentados"], 1)),
        ("Meses con más de 10 atentados", _fmt(resultado["p_mas_10"], 1) + " %"),
        ("Intervalo del total (95 %)", "± " + _fmt(resultado["ic95"], 1)),
        ("Evitados frente a la línea base",
         _fmt(resultado["evitados"], 1) + f" ({_fmt(resultado['evitados_pct'], 1)} %)"),
        ("Parámetros", f"recaudo {params['recaudo']:g} · retardo {params['retardo']:g} meses"),
        ("Réplicas / semilla", f"{params['replicas']} · {params['semilla_inicial']}"),
    ]
    y = 0.835
    for etiqueta, valor in lineas:
        fig.text(0.09, y, etiqueta, fontsize=10, color="#262626")
        fig.text(0.62, y, valor, fontsize=10, color="#1F3864", weight="bold")
        y -= 0.026

    ax = fig.add_axes([0.09, 0.27, 0.82, 0.27])
    ax.plot(range(1, len(serie) + 1), serie, color="#1F3864", lw=1.6)
    ax.fill_between(range(1, len(serie) + 1), serie, color="#1F3864", alpha=0.08)
    ax.set_xlabel("Mes simulado", fontsize=8.5, color="#595959")
    ax.set_ylabel("Atentados", fontsize=8.5, color="#595959")
    ax.tick_params(labelsize=7.5, colors="#595959")
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    ax.grid(axis="y", color="#E7EDF6")
    ax.set_axisbelow(True)
    ax.set_title("Trayectoria promedio de las réplicas", fontsize=9.5, color="#262626")

    aviso = (
        "Advertencia de alcance. Este reporte no es un pronóstico. Compara escenarios bajo una "
        "estructura calibrada con datos del periodo indicado; los valores dependen de los "
        "supuestos del modelo y no de una tendencia observada. No distingue regiones ni "
        "organizaciones. Las cifras absolutas no deben usarse como proyección de hechos."
    )
    fig.text(0.09, 0.19, aviso, fontsize=8, color="#595959", wrap=True)
    fig.text(0.09, 0.07,
             "Generado automáticamente por el DSS · Universidad de Cundinamarca · Modelación 902",
             fontsize=7.5, color="#7A8699")

    buffer = io.BytesIO()
    with PdfPages(buffer) as pdf:
        pdf.savefig(fig)
    plt.close(fig)
    return buffer.getvalue()
