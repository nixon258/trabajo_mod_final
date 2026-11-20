# DSS — Sistema de apoyo a decisiones

Capa de software sobre el modelo de simulación: una API que ejecuta escenarios y un panel web
que los compara. **Incremento 1** de la bitácora de implementación (`04_futuro`).

![Panel](docs/captura_panel.png)

## Qué hace

- Ejecuta escenarios sobre **dos modelos**: calibrado 1998–2004 (84 meses) y proyección
  2027–2031 (60 meses).
- Cambia dos parámetros: recaudo potencial (financiamiento) y retardo de la respuesta estatal.
- Corre N réplicas con semilla fija y devuelve media, varianza, meses en calma, picos e
  intervalo del 95 %.
- Compara contra la línea base del mismo modelo y calcula atentados evitados.
- Exporta CSV e imprime a PDF desde el navegador.

## Requisitos

- Python 3.10 o superior.
- Los modelos del repositorio: `02_informe/modelo_farc.py` y `04_futuro/modelo_futuro.py`.

## Instalación

```bash
cd 06_software
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecución

```bash
./run.sh
# o bien:
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Abrir `http://127.0.0.1:8000`. El panel simula el escenario base al cargar.

Parámetros por URL: `?modelo=futuro&rec=40&tau=2&rep=30`.

## API

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/salud` | Estado y modelos disponibles |
| GET | `/api/modelos` | Metadatos y valores base de cada modelo |
| POST | `/api/simular` | Ejecuta un escenario |

Ejemplo:

```bash
curl -X POST http://127.0.0.1:8000/api/simular \
  -H 'Content-Type: application/json' \
  -d '{"modelo":"futuro","recaudo":40,"retardo":2,"replicas":30}'
```

Respuesta (resumida):

```json
{"total":151.0,"media_mensual":2.52,"varianza_mensual":11.99,
 "meses_sin_atentados":8.6,"p_mas_10":6.1,"ic95":3.3,
 "evitados":58.6,"evitados_pct":28.0,"meses":60}
```

## Pruebas

```bash
python -m pytest tests -q
```

Ocho pruebas de aceptación: salud, metadatos, ambos modelos, efecto del recaudo, validación de
rangos, reproducibilidad y servicio del panel.

## Criterios de aceptación cumplidos

| Criterio | Umbral | Resultado |
|---|---|---|
| Reproducir la base (futuro) | 211 atentados | 209,6 con 30 réplicas |
| Reproducir la base (calibrado) | 290,0 atentados | 289,9 con 30 réplicas |
| Latencia por escenario | < 60 s | 31–208 ms |
| Error frente al modelo Python | < 1 % en la media | 0,7 % |
| Trazabilidad | semilla y parámetros visibles | sí, en la respuesta y en el panel |

## Límites

- No es un pronóstico: compara escenarios bajo una estructura calibrada.
- Sin autenticación ni base de datos: el incremento 1 no persiste corridas.
- Una petición a la vez por proceso; la cola de tareas es del incremento 2.
- La línea base se cachea por modelo y número de réplicas.

## Siguiente incremento

Persistencia en SQLite, historial de corridas, comparación de varios escenarios en la misma
gráfica y exportación PDF generada por el backend (semanas 5–7 de la bitácora).
