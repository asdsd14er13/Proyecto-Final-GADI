# 02. COMPARATIVA DE PROPUESTAS Y DECISIONES TÉCNICAS
**Análisis comparativo:** Planteamiento Inicial vs. Avance del Compañero vs. Propuesta Consolidada  
**Objetivo:** Definir con rigor de ingeniería qué componentes se adoptan, cuáles se descartan y por qué razones metodológicas y prácticas.

---

## 1. Tabla Comparativa de las 3 Alternativas

| Criterio de Evaluación | Alternativa A: Planteamiento Inicial (PDF Plan Técnico) | Alternativa B: Avance de la Carpeta (Compañero) | Alternativa C: Propuesta Consolidada (Solución Oficial) |
| :--- | :--- | :--- | :--- |
| **Fuentes de Datos** | 4 fuentes heterogéneas masivas: OULAD (Reino Unido), Saber Pro (Colombia), CENAUN (Perú) y ENAHO (Perú). Más de 11.8 millones de filas. | 2 fuentes: `data.csv` (UCI Dropout) y datos oficiales de TUNI/SUNEDU (`matriculado_2025_II.csv` e `institucional.csv`). | **3 fuentes complementarias:**<br>1. `data.csv` (UCI granular - rendimiento y deserción real).<br>2. TUNI/SUNEDU (Catálogo institucional de universidades peruanas).<br>3. ENAHO 2023 (INEI - Módulos 300/500 de horas de trabajo y empleo). |
| **Arquitectura de Datos** | Data Lake Medallón (Bronce, Plata, Oro) + Data Warehouse. | Staging en SQL Server + DataMart en estrella para UCI + DataMart de matrícula TUNI. | **Área de Staging + DataMart Relacional en Esquema Estrella en SQL Server** (alineado 100% a la pauta del docente). |
| **Motor de ETL** | Scripts en Python / Pipeline de Data Lake teórico. | Scripts T-SQL y Python. | **Visual Studio (SSIS - SQL Server Integration Services):** Paquetes `.dtsx` con *Flat File Sources*, *Derived Columns* y *OLE DB Destinations*. |
| **Procesamiento Analítico (OLAP)** | Tablero conceptual sin especificar cubo formal. | Tablas dimensionales en SQL Server para lectura tabular. | **SQL Server Analysis Services (SSAS) / Cubo OLAP Multidimensional:** Definición de dimensiones, jerarquías y medidas MDX/DAX. |
| **Módulo de Machine Learning** | Plantea XGBoost + Random Forest + K-Means sin código implementado. | Código implementado y verificado en `01_prototipo_analitica_adaptativa.ipynb` (Regresión Logística vs. Random Forest). | **Python (Scikit-Learn) verificado:** Comparación formal de Regresión Logística vs. Random Forest en 2 momentos temporales (Ingreso vs. 1er Semestre). Exporta predicciones a SQL Server. |
| **Canal de Consumo y Visualización** | Plataforma Web full-stack interactiva en tiempo real (microcápsulas) + Power BI. | Generación de CSVs y consultas SQL. | **Power BI Desktop:** Dashboard inteligente con KPIs institucionales, semáforo predictivo de IA y simulación interactiva What-If. |
| **Viabilidad y Riesgo** | **Inviable en plazo:** Muy alto riesgo de no entrega por dispersión en desarrollo web y problemas metodológicos de datos. | **Técnicamente viable,** pero le faltaba la conexión con SSIS, SSAS y el contexto laboral de ENAHO. | **100% Viable y Óptima:** Cumple cada punto de la rúbrica docente con las herramientas de clase y aprovecha el código ya existente. |

---

## 2. Matriz de Decisiones de Ingeniería: Qué Va, Qué No Va y Por Qué

### ❌ 1. ¿Por qué NO va el Sistema Web Interactivo Full-Stack?
* **Motivo de descarte:** El curso es *"Gestión y Análisis de Datos e Información"*, no *Ingeniería de Software* ni *Desarrollo Web*. La rúbrica evalúa modelado dimensional, ETL, cubos OLAP, métricas de Machine Learning y dashboards ejecutivos en Business Intelligence.
* **Impacto en el equipo:** Programar un frontend web adaptativo, endpoints en tiempo real y microcápsulas formativas consumiría el 70% del tiempo del grupo en tareas que el profesor no califica en la rúbrica, poniendo en riesgo los entregables obligatorios de datos.
* **Sustitución técnica:** Toda la capacidad analítica y prescriptiva se centraliza en **Power BI Desktop**, que es la herramienta corporativa estándar exigida en el criterio de Business Intelligence.

---

### ❌ 2. ¿Por qué NO va el cruce forzado de 11.8 Millones de Registros (OULAD + Saber Pro + CENAUN)?
* **Motivo de descarte:** **Inconsistencia metodológica y falacia de datos (Frankenstein de datos).**  
  * OULAD registra telemetría de clics de alumnos en el Reino Unido; Saber Pro evalúa competencias estandarizadas en Colombia; CENAUN y ENAHO son censos poblacionales en Perú.  
  * **No existe una clave primaria/foránea común:** Un estudiante británico de OULAD no tiene DNI peruano ni código de matrícula en SUNEDU. Forzar un "cruce" inventando un identificador común es metodológicamente indefendible ante un jurado de tesis o sustentación de ingeniería.
* **Sustitución técnica:** Cada fuente cumple un rol especializado sin cruces fraudulentos:
  * El dataset granular (`data.csv` de UCI) provee la trazabilidad alumno-materia-nota-deserción para el Machine Learning y la tabla de hechos académica.
  * TUNI/SUNEDU provee la jerarquía de instituciones y carreras oficiales en el Perú.
  * ENAHO provee los perfiles de sobrecarga horaria y vulnerabilidad económica nacional.

---

### ❌ 3. ¿Por qué NO se construye un Data Lake Medallón (Bronce, Plata, Oro)?
* **Motivo de descarte:** La arquitectura esperada por el profesor indica textualmente:  
  $$\text{Base Transaccional} \longrightarrow \text{ETL} \longrightarrow \text{Data Warehouse / DataMart}$$  
  Un Data Lake se justifica ante Terabytes o Petabytes de datos no estructurados (imágenes, video, logs de sensores). Para datos tabulares estructurados (CSV), la metodología formal enseñada en la cátedra (Ralph Kimball) utiliza un **Área de Staging (área de preparación)** en SQL Server, que actúa como capa intermedia limpia antes de poblar las tablas de hechos y dimensiones.

---

### ❌ 4. ¿Por qué NO se cambia la formulación a un modelo de Regresión de Notas?
* **Motivo de descarte:** Predecir si un alumno sacará $11.4$ o $11.8$ de nota final no resuelve el problema de gestión de la facultad. La decisión empresarial y de tutoría es **identificar el estado de riesgo cualitativo** para activar protocolos de retención.
* **Sustitución técnica:** Se modela como un problema de **Clasificación Supervisada Multiclase** (`Dropout`, `Enrolled`, `Graduate`), y en el dashboard se prioriza la probabilidad de abandono ($P(\text{Dropout}) \ge 0.60$) como umbral de intervención temprana.

---

### ✔️ 5. ¿Por qué SÍ va el Dataset Granular de Rendimiento (`data.csv` - UCI)?
* **Justificación técnica:** Contiene 4,424 observaciones con 36 atributos completos, notas vigesimales del primer ciclo, créditos cursados y el resultado histórico verificado. Permite construir una matriz de entrenamiento limpia sin datos inventados y obtener métricas técnicas reales (F1 macro $\approx 0.62$, Recall $\approx 0.64$).
* **Rol:** Alimenta `dw.FactProgreso` y el modelo de Machine Learning.

---

### ✔️ 6. ¿Por qué SÍ va la Fuente Oficial de TUNI / SUNEDU?
* **Justificación técnica:** Aporta la realidad universitaria peruana: catálogo de universidades públicas y privadas, facultades y carreras oficiales.
* **Rol:** Permite construir la dimensión institucional (`dw.DimInstitucionTUNI`) y un DataMart de contexto nacional universitario, otorgando identidad y pertinencia nacional al proyecto.

---

### ✔️ 7. ¿Por qué SÍ va la ENAHO 2023 (INEI)?
* **Justificación técnica:** Provee el fundamento empírico del problema en el Perú: más del $45.4\%$ de los estudiantes universitarios peruanos trabaja, promediando más de $28$ horas semanales.
* **Rol:** Alimenta la dimensión socioeconómica (`dw.DimPerfilSocioeconomico`) y sustenta los diagramas AS-IS / TO-BE y la justificación del informe ante el profesor.

---

### ✔️ 8. ¿Por qué SÍ se implementa SSIS en Visual Studio y Cubo OLAP en SSAS?
* **Justificación técnica:** Son las herramientas oficiales evaluadas en los criterios 3 y 4 de la rúbrica del profesor.
* **Rol:**
  * **SSIS:** Demuestra dominio de ETL empresarial (flujos de control, flujos de datos, conversiones y calidad de datos).
  * **SSAS (Cubo OLAP):** Demuestra capacidad de análisis multidimensional (medidas agregadas, jerarquías institucionales y consultas analíticas de alto desempeño).

---

### ✔️ 9. ¿Por qué SÍ se usa Random Forest frente a Regresión Logística?
* **Justificación técnica:**
  * La **Regresión Logística** provee una base de comparación lineal (*baseline*) transparente y rápida.
  * El **Random Forest** captura relaciones no lineales e interacciones complejas entre la carga académica y los antecedentes del estudiante, alcanzando un mayor **Recall en la clase de abandono ($64.2\%$)**, minimizando los falsos negativos (estudiantes en riesgo real que no son detectados a tiempo).

---

## 3. Síntesis de la Decisión del Equipo
La solución elegida aprovecha el **código, scripts SQL y modelos ya desarrollados en la carpeta por el compañero**, los enriquece con la **justificación socioeconómica de la ENAHO** de la propuesta inicial, y estructura toda la entrega bajo las **herramientas y rúbrica formal del Mg. Ing. Ivan Crispin Sanchez**.
