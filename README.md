# Modelación 902 — Modelo de simulación de los ciclos de violencia de las FARC, 1998–2004

**Universidad de Cundinamarca** · Facultad de Ingeniería · Ingeniería de Sistemas y Computación
**Docente:** Daniel Moncada
**Equipo:** Samuel David Segura Vargas, Juan Nicolás Bobadilla Soler,
Andrés Mauricio Reina Mayorga, Kevin Samuel Viasus Rivera

Problema regional: la violencia de las FARC entre 1998 y 2004 no fue constante, osciló en
ciclos. El trabajo modela esa oscilación y compara dos intervenciones: mayor severidad estatal
y reducción del financiamiento.

## Empezar aquí

El repositorio reúne las tres actividades de la asignatura. Para entenderlo sin leer todo,
sigue este orden:

1. `00_insumos/farc_modelo.md` — qué dice el artículo que se replica.
2. `02_informe/informe_final_act2.pdf` — modelo, calibración y resultados.
3. `03_exposicion/guion_exposicion.md` — cómo se explica el trabajo.

Requisitos para reproducir:

- Python 3 con `numpy`, para el modelo de sistemas.
- Java 17 o superior, para JaamSim.
- LibreOffice, solo si vas a editar los `.docx` o el `.pptx`.

Los comandos están en la sección «Cómo reproducir». La presentación se abre con doble clic en
`03_exposicion/presentacion_act3.html` y no necesita internet.

Estado: actividades 1 y 2 entregadas; la 3 está preparada y pendiente de exposición.

Las memorias del congreso (`00_insumos/ecds2009_memorias.pdf`) son material de referencia del
curso: no se redistribuyen fuera del equipo.

## Estructura del directorio

```
00_insumos/      Consignas del curso y material de referencia
01_bitacora/     Actividad 1: bitácora estratégica (consigna y APA 7)
02_informe/      Actividad 2: modelo, resultados e informes
03_exposicion/   Actividad 3: presentación, guion y demo
04_futuro/       Proyección 2027-2031 y bitácora de la solución de software
```

### 00_insumos
| Archivo | Contenido |
|---|---|
| `bitacora.md` | Consigna de la actividad 1 |
| `act2.md` | Consigna de la actividad 2 |
| `act3.md` | Consigna de la actividad 3 |
| `farc_modelo.md` | Ficha del artículo base (Soto Torres et al., 2009) |
| `ecds2009_memorias.pdf` | Memorias del congreso, fuente primaria |

### 01_bitacora — Actividad 1
| Archivo | Contenido |
|---|---|
| `bitacora_estrategica.docx` `.pdf` | Versión según la consigna del curso (8 págs) |
| `bitacora_estrategica_apa7.docx` `.pdf` | Versión con formato APA 7 (9 págs) |
| `bitacora_estrategica.md` | Fuente editable |

### 02_informe — Actividad 2
| Archivo | Contenido |
|---|---|
| `informe_final_act2.pdf` `.docx` | **Entregable**: informe técnico, 7 págs, 9 secciones |
| `informe_act2.pdf` `.docx` | Versión previa del informe (modelo en Python) |
| `documentacion_jaamsim.pdf` `.docx` | Documentación ampliada de la implementación |
| `modelo_farc.py` | Modelo calibrado, 5 niveles, 200 réplicas |
| `modelo_farc.mdl` | Traducción a Vensim (sin probar en la herramienta) |
| `resultados_modelo.json` | Salidas numéricas de calibración y escenarios |
| `fig_serie.png`, `fig_escenarios.png` | Figuras del informe |
| `jaamsim/` | Herramienta, modelos `.cfg`, resultados `.dat` y capturas |

Detalle de `jaamsim/`:

| Archivo | Contenido |
|---|---|
| `JaamSim.jar` | JaamSim 2026-08 (requiere Java 17+) |
| `fa_base.cfg` | Escenario línea base |
| `fa_severidad.cfg` | Mayor severidad estatal |
| `fa_financiacion.cfg` | Financiación reducida 60 % |
| `fa_*.dat` | Resultados por escenario |
| `fa_*.rep` | Reporte completo por objeto |
| `captura_*.png` | Capturas de la interfaz y de la corrida |

### 03_exposicion — Actividad 3
| Archivo | Contenido |
|---|---|
| `presentacion_act3.pptx` | 18 diapositivas editables, 16:9 |
| `presentacion_act3.html` | Misma presentación en HTML, archivo único con imágenes embebidas |
| `presentacion_act3.pdf` | Respaldo para proyectar |
| `conclusiones_explicadas.pdf` `.docx` `.md` | Texto largo de las cuatro conclusiones, con preguntas y respuestas |
| `guion_exposicion.md` | Qué decir por diapositiva, tiempos, reparto y preguntas |
| `demo_jaamsim.md` | Demo en vivo de 90 s y plan B |

### 04_futuro — Prospectiva y solución de software

| Archivo | Contenido |
|---|---|
| `proyeccion_2031.pdf` `.docx` | Proyección exploratoria 2027–2031: 4 escenarios, 200 réplicas |
| `bitacora_implementacion.pdf` `.docx` | Plan de 12 semanas del DSS, con criterios de aceptación |
| `modelo_futuro.py` | Modelo prospectivo (60 meses, calentamiento de 3) |
| `test_modelo_futuro.py` | 6 pruebas: horizonte, orden de escenarios, reproducibilidad |
| `resultados_futuro.json` | Métricas por escenario |
| `fig_trayectorias.png`, `fig_evitados.png` | Figuras del informe |

Advertencia de alcance: las FARC se desmovilizaron en 2016, así que la proyección modela el
**mecanismo** de un actor armado genérico, no a esa organización. No es un pronóstico.

Resultados: tendencial 211 atentados en 5 años; financiamiento −60 % evita 58 (28 %);
paquete institucional 63 (30 %); financiamiento −80 % 75 (36 %).

Ejecutar:

```bash
cd 04_futuro
python modelo_futuro.py --replicas 200
python test_modelo_futuro.py
```

### 05_propuesta — Solución de software

| Archivo | Contenido |
|---|---|
| `propuesta_solucion_software.md` | DSS web sobre el modelo: arquitectura de tres capas, motor híbrido SD+DES, panel *what-if* |

Es una propuesta de producto, no un entregable del curso: describe cómo llevar el prototipo a
una plataforma con API, réplicas múltiples y panel para decisores.

### 06_software — MVP del sistema de apoyo a decisiones

| Archivo | Contenido |
|---|---|
| `app/sim.py` | Envuelve los dos modelos y calcula métricas con intervalo de confianza |
| `app/main.py` | API FastAPI: salud, modelos y simulación |
| `app/static/index.html` | Panel con dos controles, gráfico, tabla y exportación CSV |
| `tests/` | 16 pruebas de aceptación |
| `app/db.py` | Persistencia SQLite del historial |
| `app/report.py` | Reporte PDF de una corrida |
| `app/etl.py` | Validación de series para recalibrar |
| `Dockerfile`, `docker-compose.yml` | Despliegue en contenedor |
| `RIESGOS.md` | Matriz de riesgos con mitigación y evidencia |
| `docs/captura_panel.png` | Captura del panel funcionando |

```bash
cd 06_software
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
./run.sh          # http://127.0.0.1:8000
```

Verificado: 209,6 atentados con 30 réplicas en el modelo futuro (base 211) y 289,9 en el
calibrado (base 290,0). Latencia por escenario: 31–208 ms. Historial, comparación de tres
escenarios, PDF y validación de CSV probados con 16 pruebas y un guion de humo.

## Presentación en HTML

Abrir `03_exposicion/presentacion_act3.html` en cualquier navegador. No necesita internet:
las imágenes van embebidas y el archivo pesa 248 kB.

| Tecla | Acción |
|---|---|
| `→` `↓` `espacio` | Siguiente diapositiva |
| `←` `↑` | Anterior |
| `F` | Pantalla completa |
| `P` | Imprimir o guardar como PDF |
| Clic | Mitad derecha avanza, mitad izquierda retrocede |

También funciona por enlace directo: `#7` abre la diapositiva 7.

## Cómo reproducir

El modelo de sistemas:

```bash
cd 02_informe
python modelo_farc.py --replicas 200
```

La simulación en JaamSim (Java 17 o superior; en esta máquina Java 11 es el default):

```bash
cd 02_informe/jaamsim
/usr/lib/jvm/java-21-openjdk/bin/java -jar JaamSim.jar fa_base.cfg
```

Para obtener resultados sin interfaz, añadir `-batch` antes del archivo `.cfg`.
Resultado esperado: 287 atentados en 84 meses y cero oportunidades en espera.

## Resultados principales

| Escenario | Atentados (JaamSim) | Media mensual | Lectura |
|---|---|---|---|
| Línea base | 287 | 3,45 | Reproduce media y meses en calma |
| Mayor severidad estatal | 267 | 3,28 | −5 %, pero el ciclo se estira |
| Financiación −60 % | 183 | 2,24 | −35 % y serie más estable |

Validación frente a la serie real: 5 de 6 criterios. La varianza reportada en el artículo
(5,43) es incompatible con su propia distribución por categorías; el informe lo demuestra.

## Estado de cada actividad

- Actividad 1: entregada (bitácora en dos versiones).
- Actividad 2: entregada (`informe_final_act2.pdf`).
- Actividad 3: preparada (presentación y guion); pendiente la exposición.
