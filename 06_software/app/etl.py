"""Validación de series de datos para calibración (contrato de ingesta).

Formato aceptado: CSV con encabezado y dos columnas, `mes` y `atentados`.
Separador coma o punto y coma. La validación no reemplaza la calibración:
diagnostica si una serie nueva es comparable con la de referencia.
"""
import csv
import io
import statistics

REFERENCIA = {"media": 3.82, "varianza": 5.43,
              "p_0_3": 0.71, "p_4_10": 0.19, "p_mas_10": 0.10, "meses_sin": 15}


def _delimitador(texto):
    primera = texto.split("\n", 1)[0]
    return ";" if primera.count(";") > primera.count(",") else ","


def validar_csv(contenido, meses_minimos=24):
    try:
        texto = contenido.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError("El archivo debe estar en UTF-8") from exc

    delimitador = _delimitador(texto)
    filas = list(csv.reader(io.StringIO(texto), delimiter=delimitador))
    if len(filas) < 2:
        raise ValueError("El archivo no contiene datos")

    encabezado = [c.strip().lower() for c in filas[0]]
    if "mes" not in encabezado or "atentados" not in encabezado:
        raise ValueError("Se esperan las columnas 'mes' y 'atentados'")
    i_mes, i_at = encabezado.index("mes"), encabezado.index("atentados")

    valores, errores = [], []
    for n, fila in enumerate(filas[1:], start=2):
        if not fila or all(not c.strip() for c in fila):
            continue
        try:
            mes = fila[i_mes].strip()
            valor = float(fila[i_at].strip().replace(",", "."))
        except (IndexError, ValueError):
            errores.append(f"fila {n}: valor no numérico")
            continue
        if valor < 0:
            errores.append(f"fila {n}: atentados negativos")
            continue
        if not mes:
            errores.append(f"fila {n}: mes vacío")
            continue
        valores.append(valor)

    if len(valores) < meses_minimos:
        raise ValueError(f"Se requieren al menos {meses_minimos} meses; llegaron {len(valores)}")

    media = statistics.fmean(valores)
    varianza = statistics.variance(valores)
    categorias = {
        "p_0_3": sum(1 for v in valores if v <= 3) / len(valores),
        "p_4_10": sum(1 for v in valores if 4 <= v <= 10) / len(valores),
        "p_mas_10": sum(1 for v in valores if v > 10) / len(valores),
        "meses_sin": sum(1 for v in valores if v == 0) / len(valores) * len(valores),
    }

    alertas = list(errores)
    if not (2.0 <= media <= 6.0):
        alertas.append("la media se aleja del rango de referencia (2 a 6 atentados por mes)")
    if varianza < media:
        alertas.append("varianza menor que la media: serie más regular que la de referencia")
    if categorias["meses_sin"] < 5:
        alertas.append("pocos meses sin atentados frente a la referencia (15 en 84 meses)")

    return {
        "valido": not errores,
        "meses": len(valores),
        "media": round(media, 2),
        "varianza": round(varianza, 2),
        "categorias": {k: round(v, 3) for k, v in categorias.items()},
        "referencia": REFERENCIA,
        "errores": errores,
        "alertas": alertas,
        "recomendacion": ("Serie comparable: se puede usar para recalibrar."
                          if not alertas else
                          "Revisar las alertas antes de recalibrar con esta serie."),
    }
