# Guion de la exposición — Actividad 3

**Curso:** Modelación 902 · **Docente:** Daniel Moncada
**Equipo:** Samuel David Segura Vargas, Juan Nicolás Bobadilla Soler, Andrés Mauricio Reina Mayorga, Kevin Samuel Viasus Rivera
**Soporte:** `presentacion_act3.pptx` (18 diapositivas) · `02_informe/jaamsim/` (modelo y resultados)

Sin tiempo fijo. El bloque núcleo son 8 minutos; cada módulo marcado *ampliable* admite 1 o 2 minutos extra si hay preguntas.

---

## Bloque núcleo (8 min)

### Diapositiva 1 — Portada (20 s)
Preséntense y anuncien la tesis en una frase: «Vamos a mostrar por qué la violencia de las
FARC se movía en ciclos y qué palanca los reduce». No lean la portada completa.

### Diapositiva 2 — El problema (50 s)
El dato que abre: 571 atentados en siete años, segundo registro del mundo. Luego giren el
enfoque: el problema no es el total, es la forma. 15 meses sin atentados, un mes con 25.
Cierren con la consecuencia: un Estado que reacciona al miedo gasta en el pico y queda sin
margen en la calma.

### Diapositiva 3 — La pregunta (30 s)
Una sola frase, lenta: «¿Qué produce el ciclo y qué lo reduce sin aumentar el miedo?».
Aclaren por qué no se puede experimentar con el sistema real. Esta diapositiva justifica todo
lo que sigue; no la apuren.

### Diapositiva 4 — Tres bucles (60 s)
Señalen cada círculo con el puntero. Refuerzo: miedo–recaudo–material. Balance 1: severidad
del Estado. Balance 2: consumo de material. La frase que deben recordar: «el ciclo emerge del
desfase, no de la violencia». Cuatro meses de retardo es el dato clave.

### Diapositiva 5 — Del sistema al evento (40 s)
Dos columnas, una idea: el modelo de sistemas dice **cuándo**, JaamSim dice **cuánto cuesta en
capacidad**. Si preguntan por qué no quedarse con uno: porque cada motor responde una pregunta
distinta y compararlos verifica la estructura.

### Diapositiva 6 — Modelo en JaamSim (40 s)
Recorran la cadena con el dedo: oportunidades, espera, comando operativo, material, atentados.
Digan qué es cada icono en una palabra. Cierren con los contadores: 281 acumulados, cero en
espera.

### Diapositiva 7 — Metodología (40 s)
Cinco fases. El dato que importa: 2.000 combinaciones de parámetros y seis criterios definidos
**antes** de calibrar. Si alguien pregunta por el sesgo de calibrar: «el criterio no se ajusta
al resultado».

### Diapositiva 8 — Validación (60 s)
Cinco de seis. Lean la tabla en dos golpes: media y meses sin atentados coinciden; la varianza
no. No esquiven la varianza: «con 71/19/10 % y máximo 25, la varianza mínima posible es 12; el
5,43 del artículo no puede venir de esa distribución». Es el punto más fuerte de la exposición.

### Diapositiva 9 — Escenarios (50 s)
Dos palancas, dos resultados. Severidad: −5 %, pero 40 meses en calma y varianza 27,6.
Financiamiento: −35 % y varianza 7,2. Conclusión: la segunda actúa sobre la causa.

### Diapositiva 10 — JaamSim vs modelo (40 s)
Tres escenarios, desviaciones de −1,0, −3,2 y −2,6 %. Y los dos hallazgos operativos: cola
cero y utilización de 0,10 de 20 comandos. Frase: «la logística nunca fue el cuello de
botella».

### Diapositiva 11 — Demostración en vivo (90 s)
Ver `demo_jaamsim.md`. Orden: abrir el modelo, ejecutar, leer contadores, mostrar el `.dat`.
Si algo falla, pasen a la diapositiva 6 y sigan con las capturas; no improvisen delante del
grupo.

### Diapositivas 12–13 — Impacto y sostenibilidad (60 s)
Cuatro cambios en la decisión pública: presupuesto, prioridad, tiempo, territorio. En
sostenibilidad, contrapongan las dos columnas y lean el criterio: institucionalidad continua
en lugar de picos de gasto.

### Diapositivas 14–17 — Conclusiones individuales (2 min, 30 s cada una)
Cada integrante lee **su tesis** y una sola bala de apoyo. La implicación en rojo se dice de
memoria, sin leer. No repitan el mismo argumento entre ustedes: son cuatro ángulos distintos
—implementación, datos, diseño, comunicación—.

### Diapositiva 18 — Cierre (20 s)
Digan dónde está todo y los tres frentes abiertos: varias réplicas, cerrar el bucle dentro de
JaamSim y aplicar el modelo a un municipio de Cundinamarca. Abran preguntas.

---

## Módulos ampliables

- **Ecuaciones (si preguntan por el detalle técnico):** muestren `02_informe/informe_final_act2.pdf`,
  sección 3.2. Expliquen solo la regla de atentados: mín(capacidad, oportunidad).
- **Calibración (si preguntan cómo eligieron parámetros):** búsqueda aleatoria sobre siete
  parámetros, función de error sobre momentos, criterios fijados antes.
- **JaamSim técnico (si preguntan por la herramienta):** el modelo es un archivo de texto;
  se ejecuta en batch sin interfaz; usa Java 21 y la versión 2026-08.

---

## Preguntas probables y respuestas

**¿Por qué no usaron Vensim o ProModel?**
Vensim es de escritorio Windows y no está disponible en el entorno del laboratorio; ProModel
guarda archivos binarios que no se pueden auditar. JaamSim es libre, corre en Linux y su
modelo es texto versionable.

**¿El modelo sirve para predecir atentados?**
No, y el artículo base lo dice: la violencia terrorista es aleatoria. Sirve para explicar el
mecanismo y comparar escenarios.

**¿Por qué la tasa de llegadas viene del otro modelo y no se calcula dentro?**
Porque el bucle de retroalimentación está calibrado en el modelo de sistemas y JaamSim aporta
el detalle operativo. Es una limitación declarada; se cierra con un `ScriptEntity` que
actualice la tasa cada mes.

**¿Por qué una sola réplica por escenario?**
Porque el objetivo era comparar el mismo escenario entre dos motores con la misma semilla.
Para intervalos de confianza hacen falta 30 o más réplicas, y está en los frentes abiertos.

**¿Qué pasa si cambia el contexto, por ejemplo después del Acuerdo de Paz?**
El modelo está calibrado con 1998–2004 y no incluye el acuerdo. La estructura —actor que se
financia con el efecto que produce y Estado que responde con retardo— sí se puede reutilizar
con nuevos parámetros.

**¿La varianza no cumplida invalida el modelo?**
No: la media, las categorías y los meses sin atentados coinciden. La varianza reportada es
incompatible con la distribución que el propio artículo reporta. Elegimos la coherencia
interna sobre un estadístico aislado, y lo dejamos escrito.

---

## Reparto sugerido

| Bloque | Quién |
|---|---|
| 1–4 (problema y estructura) | Andrés Reina |
| 5–8 (modelo y validación) | Samuel Segura y Juan Nicolás Bobadilla |
| 9–11 (resultados y demo) | Samuel Segura |
| 12–13 (impacto y sostenibilidad) | Kevin Viasus |
| 14–17 (conclusiones) | Cada integrante, la propia |
| Cierre y preguntas | Kevin Viasus modera; responde quien domine el tema |
