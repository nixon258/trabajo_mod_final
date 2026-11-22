# Guion del video — 7:06, sin voz

**Archivo:** `dss_demo_7min.mp4` · 1920×1080 · 30 fps · 7:06 · sin audio, con texto quemado.
Todo el contenido está en pantalla: no depende de narración ni de subtítulos externos.

## Estructura y tiempos

| Inicio | Fin | Bloque | Qué se ve |
|---|---|---|---|
| 0:00 | 0:18 | Apertura | Título, equipo, tesis |
| 0:18 | 0:42 | Problema | 571 atentados, 1.300 víctimas, 25 en un mes |
| 0:42 | 1:02 | Patrón | 71 / 19 / 10 % y la frase del sistema que oscila |
| 1:02 | 1:38 | Bucles | Refuerzo y dos balances; el desfase de 4 meses |
| 1:38 | 2:02 | Ecuaciones | Cinco niveles y la regla `mín(capacidad, oportunidad)` |
| 2:02 | 2:30 | Validación | Tabla real vs simulado, 5 de 6 criterios |
| 2:30 | 2:59 | Serie animada | Trazo progresivo de 84 meses contra la media 3,82 |
| 2:59 | 3:17 | JaamSim | Oportunidades, comando operativo, material |
| 3:17 | 3:25 | **JaamSim en vivo** | Captura real de la corrida: 287 atentados |
| 3:25 | 3:43 | Lectura JaamSim | Nadie hizo cola; el límite es la oportunidad |
| 3:43 | 4:01 | Software | Qué es el DSS: dos modelos, dos palancas |
| 4:01 | 4:21 | Panel base | 210 atentados en 60 meses |
| 4:21 | 4:41 | Panel recorte | 151 atentados, 28 % evitados |
| 4:41 | 5:01 | Comparación | Tres líneas y tabla de escenarios |
| 5:01 | 5:21 | Reporte | PDF de una corrida e historial |
| 5:21 | 5:51 | Prospectiva | Tabla de los cuatro escenarios |
| 5:51 | 6:21 | Prospectiva animada | Cuatro trayectorias dibujándose |
| 6:21 | 6:41 | Límites | No pronostica, no es regional, no mide costos |
| 6:41 | 7:06 | Cierre | Tesis final y enlace del repositorio |

## Cómo se generó

1. **Tarjetas**: HTML de 1920×1080 renderizado con Chromium headless (tipografía Arial, paleta
   navy del proyecto).
2. **Animaciones**: matplotlib a 30 fps, escritas directo a H.264 con ffmpeg.
3. **JaamSim**: corrida real del `.cfg` base, capturada con `grim` a 6 fps y reescalada a 1080p.
4. **Panel**: capturas del DSS en vivo con `?rec=100`, `?rec=40` y `?comparar=1`.
5. **Montaje**: ffmpeg, zoompan lento en cada tarjeta, concatenación y relleno final de 0,5 s para
   cerrar en 426,0 s exactos.

## Cómo se actualiza

Si cambia el panel o los resultados:

```bash
# 1. servidor del DSS
cd 06_software && ./run.sh

# 2. capturas nuevas (rec=100, rec=40, comparar=1)
# 3. reconstruir
cd /tmp/opencode
SOLO=c10,c11,c12 .venv/bin/python build_video.py
```

El script `build_video.py` está fuera del repositorio por ser herramienta de producción; las
piezas finales (escenas y video) sí quedan en el proyecto.

## Texto que aparece en pantalla (resumen)

> ¿Por qué la violencia se mueve en ciclos?
> 571 atentados · 1.300 víctimas · 25 en un solo mes
> 71 % de los meses: 0 a 3 atentados
> El ciclo emerge del desfase: el miedo sube rápido y la respuesta llega cuatro meses tarde
> atentados = mín(capacidad, oportunidad)
> 5 de 6 criterios de validación
> JaamSim: 287 atentados, cero oportunidades en espera
> La logística no es el cuello de botella
> Línea base 210 · financiamiento −60 % → 151
> La severidad redistribuye el ciclo; el financiamiento lo reduce
> No pronostica · no es regional · no mide costos
> Un modelo reproducible vale lo que vale su reproducción
