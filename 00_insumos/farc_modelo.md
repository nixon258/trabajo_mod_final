# Ciclos en terrorismo doméstico: un modelo para las FARC

Ficha y resumen del artículo incluido en las memorias del 7° Congreso Latinoamericano de
Dinámica de Sistemas (Santa Marta, Colombia, 2009), páginas 89–102.

---

## 1. Datos bibliográficos

| Campo | Dato |
|---|---|
| Título | Ciclos en terrorismo doméstico: un modelo para las FARC |
| Autores | Mª Dolores Soto Torres, Mª Mar Pajares de Mena, Ramón Fernández Lechón, Pedro Fernández Soto |
| Filiación | Universidad de Valladolid (España); PricewaterhouseCoopers Madrid |
| Publicación | Memorias del 7° Congreso Latinoamericano y 7° Encuentro Colombiano de Dinámica de Sistemas |
| Lugar y año | Santa Marta, Colombia, 4–7 de noviembre de 2009 |
| Editor | José Luis Díaz Polentino, Grupo SIMON, Universidad Industrial de Santander |
| ISBN | 978-958-44-5902-2 |
| Páginas | 89–102 |
| Palabras clave | Terrorismo, Dinámica de Sistemas, Simulación |
| Archivo fuente | `ecds2009_memorias.pdf`, páginas 89–102 |

Referencia en formato APA:

> Soto Torres, M. D., Pajares de Mena, M. M., Fernández Lechón, R., y Fernández Soto, P. (2009).
> Ciclos en terrorismo doméstico: un modelo para las FARC. En J. L. Díaz Polentino (Ed.),
> *Memorias del 7° Congreso Latinoamericano y 7° Encuentro Colombiano de Dinámica de Sistemas*
> (pp. 89–102). Universidad Industrial de Santander.

---

## 2. Problema abordado

Los incidentes de una organización terrorista doméstica muestran un comportamiento oscilatorio
e irregular: hay meses de alta actividad y meses sin ningún atentado. El artículo busca explicar
ese patrón a partir de la interacción entre las acciones de la organización y las medidas
contraterroristas del Estado.

Pregunta de investigación implícita: ¿qué estructura de retroalimentación genera los ciclos de
violencia de las FARC?

Datos de contexto que cita el artículo (base Global Terrorism Database, Universidad de Maryland):

- En 1998–2004, Colombia es el segundo país con más atentados (571), tras India (784).
- Las FARC, activas desde 1964, son la organización terrorista más antigua del continente.
- En 1998–2004 se les atribuyen cerca de 1.300 muertos y 1.300 heridos.
- Tres atentados con más de 100 víctimas: coche bomba en Bogotá (7 feb 2003, 32 muertos),
  cilindro de gas en la iglesia de Bojayá (2 may 2002, 119 muertos) y una serie de incidentes
  atribuidos a FARC y ELN (3 ago 1998, 275 muertos).

---

## 3. Hipótesis causal

- La organización terrorista controla **ciclos de refuerzo positivos**: el miedo de la población
  aumenta el recaudo (extorsión, rescates), que financia recursos y atentados, que a su vez
  generan más miedo.
- El Estado aplica **ciclos de balance con incertidumbre**: el miedo de la población presiona
  por medidas contraterroristas más severas, que reducen las oportunidades de atentar.
- La interacción entre ambos tipos de bucle produce la dinámica oscilatoria observada.

---

## 4. Estructura del modelo

### Variables de nivel (stocks)

| Nivel | Valor inicial | Descripción |
|---|---|---|
| Miedo | 0.65 | Miedo de la población, adimensional, entre 0 y 1 |
| Recursos económicos | 200 | Fondos de la organización |
| Recursos humanos | 150 | Miembros activos |
| Recursos materiales | 200 | Armamento y equipo |
| Reclutas | 8 | Miembros en entrenamiento |

### Variables auxiliares

- **Número de comandos**: incluye comandos operativos y de apoyo (entrenamiento, inteligencia,
  reclutamiento, custodia de secuestrados, intendencia, dirección).
- **Oportunidad de atentar**: valoración del líder sobre las condiciones; sigue una distribución
  de Poisson con media dependiente del miedo.

### Relaciones principales

- Atentados = MIN(comandos operativos, oportunidad).
- Comandos operativos = MIN(0.75 × comandos, recursos materiales / 10), con resultado entero.
- Cada comando operativo puede ejecutar como máximo un atentado mensual.

---

## 5. Ecuaciones y supuestos

Modelo en diferencias, paso de simulación mensual (`dt` = 1 mes).

### Miedo

- Flujo de entrada: creciente y cóncava respecto al daño total (atentados × daño constante por
  atentado), acotado para que el nivel no supere 1:

  ```
  MIN(1 - EXP(-Daño_total), 1 - Miedo)
  ```

- Flujo de salida (olvido): proporción decreciente del miedo:

  ```
  EXP(-Miedo) * Miedo
  ```

- Miedo = 1 representa pánico; miedo = 0, ausencia total de miedo.

### Recursos humanos

- Reclutamiento proporcional al número de miembros.
- Dos niveles conectados por un flujo: reclutas → miembros activos (tras entrenamiento).
- Flujo de salida por bajas en el nivel de miembros activos.
- Supuesto: la organización no tuvo problemas de número de miembros.

### Recursos materiales

- Entradas: adquisiciones con recursos económicos y actividades irregulares (adquisiciones sin
  costo monetario propio), modeladas como variable aleatoria normal con media y varianza fijas.
  La media garantiza unos cuatro atentados por mes, valor levemente superior a la media real.
- Salidas: depreciación y uso en atentados (gasto por atentado constante).

### Recursos económicos

- Entrada: extorsión, rescates y demás actividades, proporcional al miedo (el miedo actúa como
  proporción sobre un potencial máximo de recaudación).
- Salidas: sostenimiento de los miembros y adquisiciones.

### Gobierno

- Las medidas contraterroristas dependen del miedo: a mayor miedo, mayor severidad y menor
  oportunidad de atentar (media de Poisson más baja).

### Valores iniciales del anexo

```
Init Miedo = 0.65
Init R_economicos = 200
Init R_humanos = 150
Init R_materiales = 200
Init Reclutas = 8
```

---

## 6. Validación y resultados

Serie de datos reales (GTD, 1998–2004), distribución mensual de atentados:

| Categoría mensual | Frecuencia |
|---|---|
| 0 a 3 atentados | 71 % (incluye 15 meses sin atentados) |
| 4 a 10 atentados | 19 % |
| Más de 10 atentados | 10 % (máximo: 25 en un mes) |
| Media | 3,82 |
| Varianza | 5,43 |

Resultado de la simulación:

| Métrica | Real | Simulado |
|---|---|---|
| Media | 3,82 | 4,38 |
| Varianza | 5,43 | 5,46 |
| Meses sin incidentes | — | 13 |
| Categoría 0–3 | — | 54 casos |
| Categoría 4–10 | — | 21 casos |
| Categoría >10 | — | 6 casos |

Interpretación de los autores:

- La media y la varianza simuladas se acercan a las reales; la mayor parte del error cuadrático
  medio es asistemática.
- No hay réplica punto a punto: el error cuadrático medio calibrado es elevado.
- La estructura reproduce la forma de la distribución, no la secuencia exacta de los hechos.
- Conclusión: el modelo no sirve para pronosticar, pero sí para comprender los mecanismos del
  ciclo de violencia.

---

## 7. Limitaciones declaradas

- La violencia terrorista es por naturaleza aleatoria: no se puede predecir momento, lugar,
  objetivo ni modalidad de cada atentado.
- Varios parámetros se simplifican como constantes (daño por atentado, gasto material por
  atentado, entrenamiento de reclutas).
- Las actividades irregulares se modelan como ruido con distribución normal, sin mecanismo causal.
- El ajuste es estadístico (media, varianza, categorías), no temporal.

---

## 8. Aporte metodológico para un ejercicio propio

Sirve como plantilla para la actividad de modelo de simulación:

1. Delimitar el problema con una serie de datos observable y verificable.
2. Identificar un bucle de refuerzo (actor que se financia con el efecto que produce) y un bucle
   de balance (respuesta institucional o del entorno).
3. Definir pocos niveles con significado físico y auxiliares que concentren las decisiones.
4. Fijar el paso de simulación igual a la unidad de los datos (mensual).
5. Validar con media, varianza y distribución por categorías, no solo con ajuste punto a punto.
6. Declarar límites y supuestos en las conclusiones.

Adaptable a problemas regionales como seguridad urbana, informalidad, deserción escolar,
contaminación o uso de recursos naturales, cambiando actores y variables.

---

## 9. Referencias del artículo

1. Akcam, B. K., y Asal, V. (2005). The Dynamics of Ethnic Terrorism. *Proceedings of the
   International System Dynamics Conference*, Boston.
2. Calduch Cervera, R. (1993). *Dinámica de la Sociedad Internacional*. Ed. Ramón Areces, Madrid.
3. Das, S. P. (2008). Some mechanism of terror cycles. *Journal of Economic Behavior and
   Organization, 67*, 644–656.
4. Enders, W., y Sandler, T. (2000). Is Transnational Terrorism Becoming More Threatening?
   *The Journal of Conflict Resolution, 44*, 307–332.
5. Anderson, E. (2009). Modeling Insurgencies and Counterinsurgencies. *Proceedings of the 27th
   International System Dynamics Conference*, Albuquerque.
6. Enders, W., y Sandler, T. (2005). After 9/11: is it all different now? *The Journal of Conflict
   Resolution, 49*, 259–277.
7. Feichtinger, J., Hartl, G., Kort, P. M., y Novak, A. J. (2001). Terrorism control in the tourism
   industry. *Journal of Optimisation Theory and Applications, 108*, 283–296.
8. LaFree, G., Dugan, L., Fogg, H. V., y Scott, J. (2006). *Building a Global Terrorism Database*
   (Documento n.º 214260). University of Maryland.
9. Lofdahl, C. (2009). Implementing Irregular Warfare Policy Using Modeling and Simulation.
   *Proceedings of the 27th International System Dynamics Conference*, Albuquerque.
10. Martínez-Moyano, I. (2009). Improving Performance in Detection System. *Proceedings of the
    27th International System Dynamics Conference*, Albuquerque.
11. Prado, J. J., y Dyner, I. (2005). Evaluación de políticas públicas para el control de la carrera
    criminal en la ciudad de Medellín con apoyo de simulación. *Actas del 3° Congreso
    Latinoamericano y Encuentro Colombiano de Dinámica de Sistemas*, Cartagena de Indias.
12. Rosendorff, B. P., y Sandler, T. (2005). The political Economy of Transnational Terrorism.
    *The Journal of Conflict Resolution, 49*, 171–182.
13. Siqueira, K., y Sandler, T. (2006). Terrorism versus Government: strategic interaction,
    support and sponsorship. *The Journal of Conflict Resolution, 50*, 878–898.
14. Soto-Torres, M. D., Fernández Lechón, R., y Fernández Soto, P. (2009). Dynamics in domestic
    terrorist organizations. *Proceedings of the 27th International System Dynamics Conference*,
    Albuquerque.
15. Sterman, J. D. (2000). *Business Dynamics: Systems Thinking and Modeling for a Complex
    World*. McGraw-Hill.
16. Sterman, J. D. (2006). Learning from Evidence in a Complex World. *American Journal of
    Public Health, 16*, 505–514.

---

## 10. Fuente primaria

Texto completo extraído con:

```bash
pdftotext -f 89 -l 102 -layout ecds2009_memorias.pdf farc.txt
```

Ruta del texto extraído: `/tmp/opencode/farc.txt`.
