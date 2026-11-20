# Guía de uso para el analista

## Qué hace el sistema

Simula escenarios de violencia armada organizada y los compara con una línea base. No predice:
estima qué cambia si se modifican dos condiciones —el financiamiento del actor y la velocidad de
la respuesta estatal— bajo la estructura calibrada del modelo.

## Cómo leer un resultado

1. **Atentados en el horizonte**: total esperado en el periodo del modelo. Es una comparación de
   escenarios, no una proyección de hechos.
2. **Evitados**: diferencia frente a la línea base del mismo modelo. Se calcula con las mismas
   semillas, así que la diferencia no es ruido.
3. **Media mensual**: intensidad típica. Sirve para comparar contra la serie histórica.
4. **Meses sin atentados**: mide calma. Un escenario puede reducir el promedio y aun así tener
   pocos meses tranquilos.
5. **Varianza**: dispersión. Baja varianza significa serie más estable y planeable.
6. **Intervalo 95 %**: ruido de semilla con las réplicas elegidas. No mide error del modelo.

## Reglas prácticas

- Usa 30 réplicas para conversar y 100 para decidir. Con 10 el intervalo es ancho.
- Cambia un parámetro a la vez; si mueves los dos, no sabrás cuál causó el efecto.
- Compara siempre contra la línea base con el mismo número de réplicas.
- Descarga el PDF y archívalo: el reporte incluye parámetros y semilla.

## Qué no se puede afirmar

- Que un municipio bajará sus atentados en X unidades.
- Que el modelo demuestra causalidad.
- Que el resultado se sostendrá después de 2031.
- Que el costo de la política está incluido: no hay función de costos.

## Errores frecuentes

| Error | Corrección |
|---|---|
| Leer «evitados» como pronóstico | Es una diferencia entre escenarios simulados |
| Usar 10 réplicas para una decisión | Subir a 30 o 100 |
| Comparar modelos distintos | Los horizontes cambian (84 vs 60 meses) |
| Confundir varianza con incertidumbre | La varianza es del fenómeno, no del modelo |
