# BITÁCORA ESTRATÉGICA

**Universidad de Cundinamarca**

Facultad de Ingeniería · Ingeniería de Sistemas y Computación

Modelo de simulación de los ciclos de violencia doméstica: atentados de las FARC, 1998–2004

Creadores de Oportunidades

Integrantes: Juan Nicolás Bobadilla Soler, Andrés Mauricio Reina Mayorga, Samuel David Segura Vargas, Kevin Samuel Viasus Rivera

Docente: Daniel Moncada

Fecha: 17 de noviembre de 2026

---

## Presentación

Este documento organiza el trabajo del equipo antes de construir el modelo. Define qué se va a simular, con qué datos, en qué herramientas, quién hace cada actividad y en cuánto tiempo. La bitácora se apoya en la consigna del curso y en el artículo de Soto Torres, Pajares de Mena, Fernández Lechón y Fernández Soto (2009), que sirve como plantilla metodológica: un modelo de dinámica de sistemas con cinco niveles, paso mensual y validación estadística por media, varianza y forma de la distribución.

El alcance es acotado a propósito. El modelo no busca pronosticar atentados individuales, porque la violencia terrorista es aleatoria por naturaleza. Busca explicar el mecanismo que produce los ciclos y comparar escenarios de respuesta estatal y de financiación de la organización.

## 2. Objetivo general del modelo de simulación

Diseñar un modelo de simulación, implementado en Vensim y complementado en ProModel, que reproduzca la dinámica mensual de los atentados atribuidos a las FARC entre 1998 y 2004, para analizar cómo interactúan el miedo de la población, el financiamiento de la organización y la respuesta contraterrorista del Estado, y para evaluar escenarios de intervención con criterios de sostenibilidad e innovación.

### Objetivos específicos

1. Reconstruir la serie mensual de atentados de 1998–2004 a partir de la Global Terrorism Database y contrastarla con las cifras reportadas en el artículo base.
2. Formular el diagrama causal y el diagrama de niveles y flujos con cinco niveles: miedo, recursos económicos, recursos humanos, recursos materiales y reclutas.
3. Implementar y calibrar el modelo en Vensim con paso de simulación mensual y un horizonte de 84 meses, y validarlo por media, varianza y distribución por categorías.
4. Evaluar al menos tres escenarios de política —línea base, mayor severidad contraterrorista y reducción de las fuentes de financiación— y documentar resultados, limitaciones y aprendizajes.

### Pregunta orientadora

¿Qué estructura de retroalimentación produce los ciclos de violencia, con meses de alta actividad y meses sin ningún atentado, y qué palancas de intervención reducen la amplitud del ciclo sin aumentar el miedo de la población en el largo plazo?

### Alcance y límites

- Periodo simulado: enero de 1998 a diciembre de 2004, 84 pasos mensuales.
- Unidad de análisis: atentados por mes atribuidos a las FARC.
- Escala geográfica: nacional, porque la serie de datos disponible es nacional. La posible aplicación al departamento de Cundinamarca se discutirá como extensión, no como resultado del modelo.
- Fuera de alcance: pronóstico puntual de fecha, lugar, objetivo o modalidad de cada atentado; estimación de víctimas individuales.

## 3. Descripción del problema regional

### 3.1 La situación observada

Colombia vivió entre 1998 y 2004 uno de sus periodos de mayor intensidad del conflicto armado interno. Según la Global Terrorism Database (LaFree et al., 2006), en esos años el país registró 571 atentados, el segundo registro más alto del mundo después de India, con 784. Al mismo periodo se atribuyen cerca de 1.300 muertos y 1.300 heridos, y tres hechos de más de cien víctimas: el cilindro de gas en la iglesia de Bojayá (2 de mayo de 2002, 119 muertos), el coche bomba en Bogotá (7 de febrero de 2003, 32 muertos) y una serie de incidentes atribuidos a las FARC y al ELN (3 de agosto de 1998, 275 muertos).

Las FARC, activas desde 1964, son la organización insurgente más antigua del continente. Su operación se financió con extorsión, secuestro y vínculos con economías ilegales, y su capacidad operativa dependió de recursos humanos, materiales y económicos que se reproducían en el tiempo.

### 3.2 El patrón que se quiere explicar

La actividad de la organización no es constante. La serie reconstruida por Soto Torres et al. (2009) alterna meses sin ningún atentado con meses de más de diez, y alcanza un máximo de 25 en un solo mes. La distribución de los 84 meses del periodo es la siguiente:

**Tabla 1. Distribución mensual de atentados, 1998–2004 (serie real)**

| Categoría mensual | Frecuencia | Lectura |
|---|---|---|
| 0 a 3 atentados | 71 % | Incluye 15 meses sin ningún atentado |
| 4 a 10 atentados | 19 % | Actividad media |
| Más de 10 atentados | 10 % | Picos de alta intensidad (máximo: 25) |
| Media | 3,82 | Atentados por mes |
| Varianza | 5,43 | La varianza supera la media: comportamiento sobredisperso |

El problema no es solo la magnitud de la violencia, sino su oscilación. Un sistema que oscila castiga doble: concentra daño en los picos y deja a las instituciones sin capacidad de respuesta sostenida, porque la atención pública y el presupuesto se mueven con el miedo.

### 3.3 Población afectada y territorio

Los efectos directos recaen sobre la población civil de municipios rurales y de ciudades intermedias: víctimas fatales y heridas, desplazamiento forzado, pérdida de medios de vida y ruptura del tejido comunitario. Los efectos indirectos alcanzan a la Fuerza Pública, a los gobiernos locales y a la economía regional, que pierde inversión y transporte. En Cundinamarca, la discusión del fenómeno importa porque el departamento ha albergado históricamente corredores de movilidad de los grupos armados; el equipo tratará esa relación como hipótesis de contexto y no como resultado del modelo.

### 3.4 Por qué es importante abordarlo

- Diseño de política: permite estimar si conviene endurecer la respuesta estatal, cortar el financiamiento o combinar ambas, y con qué rezago se observan los efectos.
- Uso eficiente de recursos: los ciclos inducen sobreinversión en los picos y abandono en los valles.
- Memoria y no repetición: explicar el mecanismo ayuda a entender la violencia como sistema, no solo como suma de hechos.
- Agenda global: aporta al Objetivo de Desarrollo Sostenible 16, paz, justicia e instituciones sólidas.

### 3.5 Por qué un modelo de simulación

No es posible experimentar con el sistema real: no se puede subir o bajar la severidad del Estado para observar el efecto sobre los atentados. La simulación permite ensayar esos contrafactuales a bajo costo (Sterman, 2000), hacer explícitos los supuestos y separar lo que explica la estructura de lo que es ruido. Con datos mensuales de ocho años y una estructura de cinco niveles, la dinámica de sistemas es la técnica adecuada; ProModel se usa como complemento para el ciclo operativo de un mes, donde la decisión de atentar depende de recursos finitos y de una oportunidad aleatoria.

## 4. Plan de trabajo

### 4.1 Enfoque metodológico

El equipo sigue cinco fases: delimitar el problema con datos verificables, formular la estructura causal, implementar el modelo en la herramienta digital, validar contra la serie real y comunicar resultados con sus límites. Cada fase termina en un producto revisable, de modo que un error de una semana no se arrastre hasta el informe final.

### 4.2 Actividades

**Tabla 2. Actividades del plan de trabajo**

| Cód. | Actividad | Producto verificable | Sem. |
|---|---|---|---|
| A1 | Delimitar el problema, la pregunta y el alcance | Ficha de alcance de una página aprobada por el equipo | 1 |
| A2 | Revisar literatura y antecedentes | Seis fuentes en APA y resumen crítico del artículo base | 1 |
| A3 | Descargar y depurar la serie mensual de atentados 1998–2004 | Base depurada y tabla de media, varianza y categorías | 1–2 |
| A4 | Construir el diagrama causal y el de niveles y flujos | Diagramas y tabla de ecuaciones con unidades | 2 |
| A5 | Implementar el modelo en Vensim | Archivo .mdl con cinco niveles, dt = 1 mes y 84 pasos | 2 |
| A6 | Calibrar y validar contra la serie real | Tabla real vs. simulado y análisis de sensibilidad | 3 |
| A7 | Ejecutar escenarios contrafactuales | Tres escenarios comparados en gráficas y tabla | 3 |
| A8 | Modelar el ciclo operativo mensual en ProModel | Modelo de eventos discretos con réplicas y resultados | 3–4 |
| A9 | Redactar el informe técnico y socializar | PDF de 5 a 8 páginas y exposición de 8 minutos | 4 |

### 4.3 Variables, supuestos y reglas del modelo

El modelo replica la estructura del artículo base (Soto Torres et al., 2009). Cinco niveles acumulan el estado del sistema y los flujos los modifican mes a mes:

**Tabla 3. Niveles del modelo y valores iniciales**

| Nivel | Valor inicial | Qué representa | Origen del dato |
|---|---|---|---|
| Miedo | 0,65 | Miedo de la población, entre 0 y 1 | Calibración inicial del artículo |
| Recursos económicos | 200 | Fondos de la organización | Calibración inicial del artículo |
| Recursos humanos | 150 | Miembros activos | Calibración inicial del artículo |
| Recursos materiales | 200 | Armamento y equipo | Calibración inicial del artículo |
| Reclutas | 8 | Miembros en entrenamiento | Calibración inicial del artículo |

Reglas principales, verificadas contra el artículo y contra las unidades:

- Atentados = mín(comandos operativos, oportunidad). La oportunidad sigue una distribución de Poisson con media dependiente del miedo.
- Comandos operativos = mín(0,75 × comandos totales, recursos materiales / 10), con resultado entero. Cada comando ejecuta como máximo un atentado por mes.
- Miedo: entrada igual a mín(1 − exp(−daño total), 1 − miedo); salida por olvido igual a exp(−miedo) × miedo.
- Recursos económicos: entrada proporcional al miedo, por extorsión y rescates; salidas por sostenimiento de miembros y adquisiciones.
- Recursos humanos: reclutamiento proporcional al número de miembros, con retardo de entrenamiento entre reclutas y miembros activos.
- Recursos materiales: entradas por adquisición y actividades irregulares, modeladas como variable aleatoria normal; salidas por depreciación y gasto por atentado.

### 4.4 Criterios de validación

La validación es estadística, no punto a punto, porque la serie real es aleatoria. El modelo se acepta si cumple los siguientes umbrales, definidos antes de calibrar para no ajustar el criterio al resultado:

**Tabla 4. Criterios y umbrales de validación**

| Criterio | Métrica | Umbral de aceptación |
|---|---|---|
| Tendencia central | Media mensual de atentados | Dentro de ±15 % de 3,82 (3,25 a 4,39) |
| Dispersión | Varianza de la serie simulada | Dentro de ±20 % de 5,43 (4,34 a 6,52) |
| Forma | Porcentaje de meses en cada categoría | ±10 puntos frente a 71 / 19 / 10 |
| Meses en calma | Conteo de meses sin atentados | Entre 10 y 20 (real: 15) |
| Robustez | Sensibilidad a ±20 % en los parámetros clave | La media se mantiene en el rango aceptado |
| Consistencia | Revisión ecuación por ecuación contra el artículo | 100 % de los flujos justificados con unidades |

### 4.5 Riesgos y control

**Tabla 5. Riesgos del plan y medidas de mitigación**

| Riesgo | Prob. / impacto | Mitigación |
|---|---|---|
| Acceso restringido a la Global Terrorism Database | Alta / medio | Usar el anexo de datos del artículo y la serie publicada; documentar la fuente en APA |
| La calibración no reproduce media y varianza | Media / alto | Calibrar sobre momentos y no sobre la serie; análisis de sensibilidad; reportar el error |
| Licencias limitadas de Vensim o ProModel | Media / medio | Trabajar con versiones educativas; si falla, replicar el modelo en hoja de cálculo |
| Carga académica dispersa al equipo | Media / medio | Reunión semanal fija y tablero de tareas con fechas |

## 5. Asignación de roles y responsabilidades

Cada integrante tiene un rol primario con un producto a cargo y un rol de apoyo en las actividades de otro. Ninguna actividad queda con un solo responsable sin respaldo.

**Tabla 6. Roles, entregables y carga estimada**

| Integrante | Rol | Actividades | Entregable principal | Horas |
|---|---|---|---|---|
| Juan Nicolás Bobadilla Soler | Investigación y gestión de datos | A1, A3, A6, A7, A9 | Base depurada y validación estadística | 17,5 |
| Andrés Mauricio Reina Mayorga | Diseño conceptual del modelo | A1, A3, A4, A5, A7, A9 | Diagramas y tabla de ecuaciones | 16,5 |
| Samuel David Segura Vargas | Implementación y simulación | A1, A5, A6, A7, A8, A9 | Modelo en Vensim y en ProModel | 17,5 |
| Kevin Samuel Viasus Rivera | Validación, documentación y comunicación | A1, A2, A7, A8, A9 | Informe técnico y presentación | 17,5 |

Carga total del equipo: 69 horas, entre 16,5 y 17,5 horas por integrante. La distribución es equilibrada y cada rol concentra un tipo de tarea, lo que evita duplicar trabajo y facilita la revisión cruzada.

### Reglas de trabajo en equipo

- Reunión semanal de una hora, con acta breve y decisiones registradas.
- Un tablero compartido con las nueve actividades y su estado: pendiente, en curso, en revisión, cerrado.
- Revisión cruzada obligatoria: ningún producto se entrega sin la lectura de un integrante distinto al autor.
- Control de versiones de los archivos del modelo, con nombre y fecha en cada iteración.
- Toda decisión que cambie el alcance se anota en la sección 7 de esta bitácora.

## 6. Cronograma de actividades

El cronograma ocupa cuatro semanas. Si el docente fija un plazo distinto, se ajusta la duración de las semanas 2 y 3, que son las que admiten compresión, y se mantiene la semana 4 para redacción y socialización.

**Tabla 7. Cronograma semanal**

| Semana | Actividades | Hito o entregable | Horas |
|---|---|---|---|
| 1 | A1, A2, A3 | Problema delimitado, fuentes revisadas y serie de datos depurada | 19 |
| 2 | A4, A5 | Diagramas aprobados y modelo funcionando en Vensim | 18 |
| 3 | A6, A7, A8 | Validación, escenarios y modelo de eventos discretos | 22 |
| 4 | A9 | Informe en PDF y socialización en clase | 10 |

Los hitos son acumulativos: si un hito no se cierra, la semana siguiente absorbe el pendiente y se recorta el alcance de los escenarios, nunca la validación. La validación es el producto que sostiene la nota del informe técnico.

### Dependencias entre actividades

- A3 y A4 pueden avanzar en paralelo; A5 depende de A4.
- A6 depende de A5 y de A3: sin serie depurada no hay contra qué comparar.
- A7 depende de A6: no se simulan escenarios sobre un modelo sin calibrar.
- A8 avanza en paralelo con A6 y A7, porque usa otra herramienta y otro nivel de detalle.
- A9 integra todo y no puede empezar antes del cierre de A6.

## 7. Socialización y registro de ajustes

La bitácora se presenta en clase en la semana 4. El equipo registra cada recomendación del docente y de los compañeros, decide si la acepta y deja constancia del cambio. Este registro es la evidencia de que la planeación se revisó y no solo se escribió.

### 7.1 Ajustes previstos antes de la socialización

El equipo identificó de antemano los tres ajustes más probables, para llegar a la sesión con una respuesta preparada:

**Tabla 8. Ajustes previstos**

| Recomendación esperada | Ajuste que aplicaría el equipo | Responsable |
|---|---|---|
| Aplicar el modelo a un municipio o al departamento | Delimitar un estudio de caso con datos locales y declararlo como extensión, no como resultado | Bobadilla |
| Incluir más escenarios de política | Agregar un escenario de reducción de reclutamiento y otro de desmovilización parcial | Reina |
| Justificar el uso de dos herramientas | Documentar el reparto: Vensim para la retroalimentación, ProModel para el ciclo operativo mensual | Segura |

### 7.2 Registro de la socialización

Tabla para diligenciar durante y después de la presentación en clase:

**Tabla 9. Registro de recomendaciones y cambios comprometidos**

| Fecha | Quién recomienda | Recomendación | Decisión y ajuste | Responsable |
|---|---|---|---|---|
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |

### 7.3 Compromisos del equipo

- Cada ajuste aceptado se incorpora al plan y al cronograma en un plazo máximo de dos días.
- Los cambios que afecten el alcance se comunican a todo el equipo en la reunión semanal.
- La versión final de la bitácora se archiva junto con el informe técnico, como anexo del proceso.

## Referencias

LaFree, G., Dugan, L., Fogg, H. V. y Scott, J. (2006). *Building a Global Terrorism Database* (Documento n.º 214260). University of Maryland.

Soto Torres, M. D., Pajares de Mena, M. M., Fernández Lechón, R. y Fernández Soto, P. (2009). Ciclos en terrorismo doméstico: un modelo para las FARC. En J. L. Díaz Polentino (Ed.), *Memorias del 7.º Congreso Latinoamericano y 7.º Encuentro Colombiano de Dinámica de Sistemas* (pp. 89–102). Universidad Industrial de Santander.

Sterman, J. D. (2000). *Business dynamics: Systems thinking and modeling for a complex world*. McGraw-Hill.

Ventana Systems. (s. f.). *Vensim PLE: Guía del usuario*. Ventana Systems, Inc.

ProModel Corporation. (s. f.). *ProModel: Guía del usuario*. ProModel Corporation.
