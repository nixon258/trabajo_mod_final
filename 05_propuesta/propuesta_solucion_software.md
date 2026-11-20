# Propuesta de Solución de Software: Sistema de Apoyo a la Decisión (DSS) basado en Simulación Híbrida

## 1. Visión General y Propósito
El objetivo de esta propuesta es transformar el modelo académico de simulación (actualmente operado mediante scripts, ecuaciones desacopladas y ejecución manual en consola de JaamSim) en una **plataforma web interactiva de apoyo a la toma de decisiones (*Decision Support System* - DSS)**. 

Esta herramienta permitirá a analistas de seguridad, gobernaciones y alcaldías (como en el contexto departamental de Cundinamarca) evaluar el impacto de políticas públicas e intervenciones institucionales en tiempo real, eliminando la necesidad de manipular código o archivos de configuración manualmente.

---

## 2. Arquitectura del Sistema (3 Capas)

Para resolver las limitaciones actuales de ejecución estática y réplica única, se propone una arquitectura desacoplada orientada a servicios:

### A. Capa de Datos e Ingesta (ETL y Persistencia)
* **Ingesta Automatizada:** Sustitución de los archivos planos históricos estáticos por conectores (pipelines ETL) y APIs que reciban datos periódicos de fuentes oficiales (registros de incidentes, reportes de inteligencia financiera, indicadores socioeconómicos departamentales y municipales).
* **Base de Datos de Escenarios y Series de Tiempo:** Almacenamiento estructurado (ej. PostgreSQL / TimescaleDB) para guardar tanto los datos históricos de calibración como las configuraciones y resultados de las simulaciones ejecutadas por los usuarios.

### B. Motor de Simulación Híbrido (Backend & Orquestación)
El núcleo computacional automatiza el flujo entre los dos paradigmas de modelado y aprovecha las capacidades nativas de línea de comandos de JaamSim:
1. **Acoplamiento Dinámico (SD + DES):** Un orquestador (desarrollado en Python o Java) ejecuta el modelo de **Dinámica de Sistemas (SD)** para calcular las tasas de transición variables en el tiempo y las inyecta dinámicamente en el modelo de **Eventos Discretos (DES)** (ya sea mediante la generación programática de archivos `.cfg` o utilizando un `ScriptEntity` en JaamSim para actualizar parámetros mes a mes).
2. **Ejecución en Modo Headless (`-batch`):** El motor invoca a JaamSim sin interfaz gráfica (`-batch`), tratando el archivo de configuración `.cfg` como infraestructura como código.
3. **Paralelización y Análisis de Monte Carlo:** En lugar de correr una sola réplica manual, el backend lanza múltiples instancias en paralelo (decenas o cientos de réplicas con diferentes semillas aleatorias) utilizando contenedores (Docker) o colas de tareas (ej. Celery / RabbitMQ).
4. **Procesamiento de Salidas:** Un *parser* lee automáticamente los archivos de reporte estructurados (`.dat` y `.rep`) generados por JaamSim, calcula promedios, desviaciones estándar e intervalos de confianza, y los expone vía API REST.

### C. Interfaz de Usuario y Visualización (Frontend)
Una aplicación web intuitiva diseñada para tomadores de decisiones sin perfil técnico en simulación:
* **Panel de Control de Políticas (*What-If Analysis*):** Controles interactivos (*sliders*, selectores y campos numéricos) para modificar variables clave en tiempo real, por ejemplo:
  * *¿Qué ocurre si se incrementa el control financiero en un 40 %?*
  * *¿Cuál es el impacto de reducir el tiempo de respuesta institucional de 4 meses a 1 mes?*
* **Tableros Comparativos:** Gráficas dinámicas que muestran la evolución temporal de los indicadores clave, comparando el **escenario base** frente a los **escenarios simulados**, incluyendo bandas de confianza estadística producto de las múltiples réplicas.
* **Exportación de Reportes:** Generación automática de informes ejecutivos (PDF/Excel) con los parámetros evaluados y las proyecciones obtenidas.

---

## 3. Flujo de Operación de la Plataforma

1. **Configuración:** El usuario ingresa al portal web, selecciona una región o escenario base y ajusta los deslizadores de intervención institucional.
2. **Petición:** El frontend envía los parámetros en formato JSON a través de una API REST hacia el backend.
3. **Orquestación y Simulación:**
   * El backend recalcula las tasas en el módulo de Dinámica de Sistemas.
   * Genera dinámicamente las variantes del archivo `.cfg` con las semillas aleatorias configuradas.
   * Ejecuta $N$ réplicas en paralelo de JaamSim en modo `-batch`.
4. **Consolidación:** Al finalizar las ejecuciones, el sistema recolecta los archivos `.dat` y `.rep`, calcula las métricas estadísticas agregadas y guarda los resultados en la base de datos.
5. **Visualización:** El frontend recibe la respuesta y actualiza los gráficos comparativos en pantalla.

---

## 4. Ventajas Estratégicas de la Arquitectura Actual como Base

La forma en que fue diseñado el prototipo actual facilita directamente su evolución hacia un producto de software empresarial por tres razones clave:

* **Modelo como Código (*Model-as-Code*):** Toda la lógica de JaamSim reside en un archivo de texto plano (`.cfg`) ligero (~4,7 kB), lo que permite versionarlo (Git), auditarlo y modificarlo programáticamente mediante plantillas desde cualquier lenguaje de programación.
* **Desacoplamiento Nativo de la Interfaz:** Al soportar ejecución por línea de comandos (`-batch`) y emitir resultados en texto estructurado (`.dat` / `.rep`), el motor de simulación ya opera en la práctica como un **microservicio independiente**, listo para ser envuelto en una API sin necesidad de reescribir la lógica matemática ni de eventos discretos.
* **Escalabilidad Horizontal:** Al ser un proceso ligero por consola, es trivial empaquetar JaamSim en un contenedor ligero (Docker) y escalar horizontalmente el número de réplicas simultáneas según la demanda de los usuarios.