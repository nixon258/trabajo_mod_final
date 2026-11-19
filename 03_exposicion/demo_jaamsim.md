# Demostración en vivo de JaamSim

Secuencia de 90 segundos para la exposición. Ensayarla una vez antes de clase.

## Antes de la clase (5 minutos)

1. Java 21 instalado y funcionando:

```bash
/usr/lib/jvm/java-21-openjdk/bin/java -version
```

Debe responder `openjdk version "21.0.13"` o superior. Si dice 11, usen la ruta completa:
el `java` del sistema es la versión 11 y JaamSim no arranca con ella.

2. Verificar que el modelo corre sin interfaz:

```bash
cd /home/juanb/Documents/modelacion/02_informe/jaamsim
/usr/lib/jvm/java-21-openjdk/bin/java -jar JaamSim.jar -batch fa_base.cfg
cat fa_base.dat
```

Debe mostrar una fila con `287` atentados. Si falla, revisar `fa_base.log`: el error indica el
objeto y la palabra clave.

3. Tener abiertas dos ventanas de terminal en la carpeta `jaamsim` y el explorador de archivos
en la misma carpeta.

## Durante la exposición (90 s)

**Paso 1 — Abrir el modelo (25 s)**

```bash
/usr/lib/jvm/java-21-openjdk/bin/java -jar JaamSim.jar fa_base.cfg
```

Esperen a que aparezca la vista. Señalen la cadena: `Oportunidades → Espera →
ComandoOperativo → Atentados`, con `Material` y `Llegadas` arriba. Digan: «cada icono es un
objeto del modelo; el archivo que lo define es texto, no un binario».

**Paso 2 — Ejecutar (15 s)**

Clic en **Run** (botón de reproducción, arriba a la izquierda) o barra espaciadora con la
ventana del panel activa. La corrida de 84 meses termina al instante porque la simulación no
está en tiempo real.

**Paso 3 — Leer contadores (30 s)**

En la vista, abajo a la derecha: `Atentados acumulados` y `Oportunidades en espera`. Al final
de la corrida el acumulado del fotograma es 281 (mes 83,5) y el total del archivo es 287
(mes 84). Expliquen la diferencia si alguien la nota: el fotograma se toma antes del último
medio mes.

**Paso 4 — Mostrar resultados (20 s)**

```bash
cat fa_base.dat
```

Una fila con 287 atentados, cola de espera 0 y utilización del comando operativo 0,10. Luego:

```bash
for f in fa_severidad fa_financiacion; do echo "== $f"; cat $f.dat; done
```

267 y 183. Frase de cierre: «misma estructura, tres escenarios, 3,2 % de error máximo frente
al modelo calibrado».

## Plan B si algo falla

| Falla | Qué hacer |
|---|---|
| No arranca: `UnsupportedClassVersionError` | Usar la ruta `/usr/lib/jvm/java-21-openjdk/bin/java` |
| No abre ventana | Pasar a la diapositiva 6 (captura del modelo) y seguir con el `.dat` |
| El equipo no responde | Mostrar las capturas de las diapositivas 6 y 10 y los archivos `.dat` |
| Preguntan por el registro de la corrida | `fa_base.rep` tiene todos los indicadores de cada objeto |

## Después de la demo

Cerrar la aplicación con `Alt+F4` o desde el menú File. Si quedó un proceso abierto:

```bash
pgrep -x java
```

y terminar solo el proceso de JaamSim por su PID (`kill -TERM <pid>`). No usar
`pkill -f JaamSim.jar` desde una terminal que contenga ese texto: el comando se mata a sí mismo.

## Archivos que se muestran

| Archivo | Qué contiene |
|---|---|
| `fa_base.cfg` | Modelo completo, escenario línea base (4,7 kB) |
| `fa_severidad.cfg` | Mismo modelo, `k severidad` de 34,5 a 54 |
| `fa_financiacion.cfg` | Mismo modelo, recaudo de 100 a 40 |
| `fa_base.dat` | Resultados numéricos de la corrida |
| `fa_base.rep` | Reporte completo por objeto |
| `captura_*.png` | Capturas usadas en las diapositivas |
