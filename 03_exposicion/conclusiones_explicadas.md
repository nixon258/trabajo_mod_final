# Las cuatro conclusiones, explicadas

Material de apoyo para la exposición. Cada integrante defiende la suya: qué afirma, de dónde
sale, qué cifras tener a mano, qué no conviene afirmar y cómo responder.

---

## 1. Samuel David Segura Vargas — Implementación y simulación

### La tesis
**«La traducción a eventos discretos no repitió el modelo: lo auditó.»**

Repetir un modelo es volver a obtener los mismos números. Auditar es descubrir qué supuestos
estaban haciendo trabajo real y cuáles eran decorativos. Al pasar el modelo de sistemas a
JaamSim, el equipo se vio obligado a declarar explícitamente cosas que en las ecuaciones
estaban escondidas: cuántos comandos operativos existen, cuánto material hay, cuánto dura una
operación y cuántas oportunidades pueden estar en curso al mismo tiempo. Ese ejercicio mostró
que el límite del sistema no estaba donde parecía.

### De dónde sale
En el modelo de sistemas, la regla de capacidad es
`capacidad = mín(0,75 · 0,30 · H, material / 10)`. Con H = 150 miembros y 200 unidades de
material, esa regla da unos 20 comandos operativos por mes. La demanda del modelo es de 3,45
atentados por mes. Es decir: **la capacidad era entre cinco y seis veces mayor que la
demanda**. La restricción existía en la ecuación, pero nunca se activaba.

En JaamSim eso se puede medir, cosa que la ecuación no permite. Los resultados:

- Utilización del comando operativo: **0,10 de 20 puestos** ocupados en promedio.
- Longitud media de la cola de espera: **0** en los tres escenarios.
- Material en uso: **0,10 unidades de 200** en promedio; en el fotograma final, 0.

Ningún escenario hizo cola. Si la capacidad fuera el cuello de botella, la cola habría crecido
en los picos. No ocurrió.

### Qué significa
El sistema no se detiene por falta de comandos ni de material: se detiene porque **no hay
oportunidad de atentar**. La oportunidad la gobiernan el miedo de la población y la severidad
del Estado, que son los dos bucles de balance del modelo. Dicho de otro modo: la logística pone
un techo muy alto; la política pone el techo real.

La auditoría también mostró algo más fino: la restricción de capacidad **estaba latente**. En
el escenario de financiación reducida, la utilización cae de 0,103 a 0,065 porque el modelo de
sistemas baja la tasa de llegadas. Es decir, el financiamiento no actúa en JaamSim por
agotamiento de material, sino porque reduce la actividad que el otro modelo calcula. Esa
diferencia es importante y hay que decirla.

### Qué no conviene afirmar
No digas que JaamSim «demostró» que la logística no importa. Lo que muestra es que, con estos
parámetros y este horizonte, la logística no restringe. Si la demanda hubiera sido de 20
atentados por mes, el resultado sería el contrario.

Tampoco afirmes que el modelo de JaamSim reproduce el agotamiento de materiales: en la versión
implementada el material es un recurso de concurrencia (se toma y se libera), no un acopio que
se vacía. El agotamiento está en el modelo de sistemas. Es una limitación declarada y el
siguiente paso del trabajo.

### Si preguntan
**¿Entonces JaamSim no aportó nada?**
Aportó dos cosas. Primero, hizo visible una holgura que las ecuaciones ocultaban: el modelo
agregado no dice si la capacidad está al límite o al 10 %. Segundo, obligó a declarar supuestos
que estaban implícitos (número de comandos, duración de la operación, unidades de material por
atentado). Un modelo que no se puede auditar no se puede defender.

**¿Por qué los totales no coinciden exactamente con el modelo de sistemas?**
Porque JaamSim sortea cada llegada con una distribución no estacionaria y produce una
realización concreta, mientras el otro modelo trabaja con esperanzas mensuales. Las
desviaciones son −1,0 %, −3,2 % y −2,6 %, dentro del ruido de un proceso de Poisson con media
cercana a 290.

**¿Qué haría falta para cerrar la brecha?**
Dos cosas: modelar el material como un acopio consumible con reposición mensual, y realimentar
la tasa de llegadas dentro de JaamSim con un `ScriptEntity`. Está en los frentes abiertos.

### Frase de cierre
«Simular en dos motores no es repetir el resultado: es preguntarle al modelo qué supuestos
estaban trabajando de verdad.»

---

## 2. Juan Nicolás Bobadilla Soler — Investigación y datos

### La tesis
**«La varianza del artículo no puede existir con su propia distribución.»**

El artículo base reporta tres cosas a la vez: una distribución por categorías (71 % de meses
con 0 a 3 atentados, 19 % con 4 a 10, 10 % con más de 10), un máximo de 25 atentados en un mes
y una varianza de 5,43 con media 3,82. Esas tres afirmaciones no son compatibles entre sí.
Nuestro modelo «falla» en varianza porque el valor de referencia no puede provenir de la serie
que el propio artículo describe.

### El cálculo, paso a paso
La varianza se calcula como `E[x²] − μ²`. Con media fija de 3,82, lo único que se puede mover
es el segundo momento. Para que la varianza sea lo más pequeña posible hay que acercar todos
los valores a la media, pero las categorías lo impiden:

- El 71 % de los meses no puede pasar de 3.
- El 19 % no puede bajar de 4.
- El 10 % no puede bajar de 11 (es «más de 10»).
- La media debe seguir siendo 3,82.

Con esas restricciones, el reparto que **minimiza** la varianza es 71 % en 2,76, 19 % en 4 y
10 % en 11. Ese reparto da **varianza 5,96**, todavía por encima del 5,43 reportado. No existe
ninguna combinación válida que produzca 5,43 con esas categorías: el mínimo posible ya lo
supera.

Si se usan valores representativos en lugar de los extremos —1,9, 6,5 y 12,5 atentados, que es
lo que uno esperaría en cada rango—, la varianza implícita es **11,6**, y nuestro modelo da
13,93. Está más cerca de la realidad que el 5,43 del artículo.

### Por qué esto importa para el trabajo
Porque cambia la forma de validar. Si el equipo hubiera tomado la varianza como criterio único,
habría concluido que el modelo está mal y habría seguido calibrando hasta deformar la serie.
Al revisar los datos se encontró que el problema estaba en la referencia. Por eso la validación
se hizo con seis criterios y no con uno: media, tres categorías, meses sin atentados y varianza.

### Qué no conviene afirmar
No digas que el artículo «está mal» ni que los autores «se equivocaron». Lo defendible es: las
cifras reportadas **no son mutuamente compatibles**; probablemente la varianza se calculó sobre
otro corte de la serie (otro periodo, otra fuente o una serie sin desagregar por mes). Es un
problema de trazabilidad del dato, no de mala fe.

Tampoco afirmes que nuestro 13,93 es «la varianza verdadera». Es la varianza de nuestro modelo,
que reproduce mejor la forma y la cola que el estadístico aislado.

### Si preguntan
**¿Cómo calculaste el mínimo?**
Con la restricción de media y los bordes de cada categoría. Se prueban los valores extremos que
permiten acercarse a la media: 3 en la primera categoría, 4 en la segunda y 11 en la tercera;
al no cuadrar la media, se resuelve el sistema y queda 2,76, 4 y 11. Da 5,96.

**¿Y si los datos reales tienen otra desagregación?**
Entonces el 5,43 puede ser correcto, pero para otra serie. Para la que el artículo describe
—71/19/10 y máximo 25— no lo es. Ese es el punto: la inconsistencia está entre las cifras
publicadas, no en nuestra aritmética.

**¿No es riesgoso discutirle al artículo?**
Es más riesgoso aceptar un criterio que no se puede reproducir. El trabajo reporta el desajuste
y explica por qué, en lugar de esconderlo. Eso es análisis, no excusa.

### Frase de cierre
«La curaduría del dato es parte del modelado. Si el patrón de referencia no es coherente
consigo mismo, el modelo que lo contradice puede estar en lo correcto.»

---

## 3. Andrés Mauricio Reina Mayorga — Diseño conceptual

### La tesis
**«El ciclo no lo produce la violencia: lo produce el retardo con que el Estado responde.»**

La violencia no oscila por sí sola. Oscila porque hay un actor que se financia con el miedo que
produce (bucle de refuerzo) y un Estado que responde cuando el miedo ya subió (bucle de
balance), pero responde **tarde**. Ese desfase convierte una respuesta que debería estabilizar
en un mecanismo que amplifica.

### De dónde sale
El modelo tiene una variable de severidad que sigue al miedo con un retardo de **cuatro meses**
(`Severidad(t) = Severidad(t−1) + (Miedo − Severidad)/4`). Ese retardo es lo que produce la
oscilación: cuando la severidad llega, la violencia ya cambió de fase y el Estado está
gastando contra el ciclo anterior.

En el escenario de mayor severidad (k de 34,5 a 54, es decir, la oportunidad de atentar cae
más rápido cuando la severidad sube):

- Media: 3,28 atentados por mes, apenas 5 % menos que la base.
- Meses en calma: de 15,3 a 40,1. La calma se multiplica por 2,6.
- Varianza: de 13,9 a 27,6. Los picos se separan y se hacen más marcados.

Ese es el efecto péndulo: menos violencia promedio, pero más concentrada. El ciclo no se cierra,
se estira.

### Por qué el financiamiento sí funciona
Porque ataca el bucle de refuerzo, no el de balance. Si la organización no puede reponer
material ni sostener comandos, la capacidad de rearmar los picos cae de forma permanente. En el
escenario de financiación reducida: media 2,24 (−35 %), varianza 7,2 y miedo promedio 0,43. La
serie se estabiliza, no solo se desplaza.

### Qué no conviene afirmar
No digas que la severidad estatal «no sirve». Sirve para contener picos y proteger población;
lo que el modelo muestra es que **sola no cierra el ciclo**. Tampoco afirmes que el retardo es
exactamente cuatro meses en la realidad: cuatro es el valor calibrado con esta serie, no una
constante histórica.

### Si preguntan
**¿Por qué cuatro meses y no dos o seis?**
Porque es el valor que mejor reproduce la serie con los otros parámetros calibrados. Si el
retardo baja, el ciclo se acorta y la varianza disminuye; si sube, se alarga. El parámetro se
calibró, no se eligió a gusto.

**¿Por qué un retardo produce oscilación y no simplemente lentitud?**
Porque el sistema tiene memoria. La severidad se calcula sobre el miedo pasado, y el miedo
depende de los atentados, que dependen de la oportunidad, que depende de la severidad. Cuando
la respuesta llega, la condición que la motivó ya cambió: el sistema sobrerreacciona y luego
corrige. Eso es un oscilador.

**¿Eso significa que hay que responder rápido?**
Significa que hay que **anticipar**. Una respuesta rápida y proporcionada reduce la amplitud;
una respuesta tardía y fuerte la traslada. La política sostenible combina anticipación con
afectación de las rentas.

### Frase de cierre
«El Estado no falla por responder poco: falla por responder cuando el ciclo ya cambió de fase.
La palanca con efecto duradero es económica.»

---

## 4. Kevin Samuel Viasus Rivera — Documentación y comunicación

### La tesis
**«Un modelo vale lo que vale su reproducción.»**

Un resultado que no se puede volver a obtener no es evidencia: es una anécdota. La decisión de
escribir el modelo como archivo de texto —y no como una caja negra con clics— es lo que permite
que el trabajo se audite, se corrija y se actualice sin depender de quien lo hizo.

### De dónde sale
El modelo completo de JaamSim es un archivo `.cfg` de **4,7 kB**: legible, versionable,
comparable línea por línea. Los tres escenarios son tres archivos que cambian dos parámetros
(`k severidad` y `recaudo potencial`). Los resultados se escriben en `.dat` y el reporte
completo de todos los objetos queda en `.rep`.

Para reproducirlo bastan dos comandos, y cualquier integrante del grupo puede hacerlo:

```
cd 02_informe/jaamsim
/usr/lib/jvm/java-21-openjdk/bin/java -jar JaamSim.jar -batch fa_base.cfg
```

Resultado esperado: 287 atentados en 84 meses, cola de espera 0.

Las capturas que se muestran en la exposición no son recortes de pantalla del escritorio: las
genera el propio simulador con el objeto `VideoRecorder`, que guarda fotogramas PNG de la vista.
Eso significa que la imagen se puede volver a producir con la misma corrida.

### Por qué esto es un argumento y no un trámite
Porque la reproducibilidad cambia el estatus del trabajo. Un modelo que se reproduce se puede
contradecir con datos; uno que no, solo se puede creer o descreer. Y porque documentar los
límites —una réplica por escenario, tasa heredada del modelo calibrado, un día simulado por
mes— evita que otro equipo use el resultado como si fuera un pronóstico.

### Qué no conviene afirmar
No digas que el modelo es «validado» en general: está calibrado y validado contra una serie
específica, con cinco de seis criterios. Tampoco prometas que sirve para predecir atentados:
no es su propósito ni lo permite la naturaleza del fenómeno.

### Si preguntan
**¿Por qué no lo hicieron en Excel?**
Porque Excel no deja auditar la lógica: las fórmulas viven en celdas y el modelo no se puede
comparar entre versiones. El `.cfg` es texto y se ve completo en una pantalla.

**¿Qué pasa si JaamSim cambia de versión?**
El archivo declara la versión usada (2026-08) y el modelo se puede migrar. Al ser texto, el
cambio queda a la vista; con un binario no.

**¿Cómo se sabe que los resultados no están manipulados?**
Porque la semilla es fija (3), los tres escenarios usan la misma y el `.rep` conserva todos los
indicadores de cada objeto. Cualquiera repite la corrida y compara.

**¿Documentar las limitaciones no debilita la presentación?**
Al contrario: le pone techo a lo que se puede afirmar. Un modelo sin límites declarados es un
modelo del que no se puede confiar en nada.

### Frase de cierre
«Si no se puede reproducir, no es evidencia. La documentación no acompaña al modelo: es parte
del modelo.»

---

## Cómo usar este documento

1. Cada integrante lee solo su sección y la explica en voz alta una vez, sin mirar el texto.
2. Si se traba, vuelve a la lista «Si preguntan»: allí están las tres o cuatro objeciones
   probables.
3. En la exposición, la tesis se dice de memoria; las cifras se consultan en la diapositiva.
4. Si una pregunta no tiene respuesta, la respuesta correcta es: «no lo medimos; queda como
   frente abierto». Es más creíble que improvisar.
