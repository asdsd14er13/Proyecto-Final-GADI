# FICHA DE ALCANCE Y ALINEACIÓN METODOLÓGICA (FASE A0)

**Curso:** Gestión y Análisis de Datos e Información (GADI) – 2026  
**Docente:** Mg. Ing. Ivan Crispin Sanchez  
**Institución:** Universidad Nacional Federico Villarreal (UNFV)  
**Facultad:** Facultad de Ingeniería Electrónica e Informática (FIEI)  
**Documento Fuente:** `Proyecto_Final_GADI_IA_2026.docx` / `05_PLAN_MAESTRO_DESARROLLO.md`  
**Estado:** Cerrado y Aprobado (Hito A0 Completado)

---

## 1. Título Oficial y Subtítulo de Alcance Técnico (Decisión D1)

* **Título Oficial (Asignado por la Cátedra):**  
  **"Sistema Inteligente de Evaluación Adaptativa y Personalización del Aprendizaje Universitario"**
* **Subtítulo de Alcance Técnico y Aplicación:**  
  *Plataforma Integral de Business Intelligence y Machine Learning basada en DataMart Multidimensional, Pipelines SSIS, Cubos OLAP y Modelos Predictivos para la Gestión de Retención Académica en UNFV-FIEI*

---

## 2. Definiciones Operativas Fundamentales (Decisiones D2 y D3)

Para garantizar la coherencia metodológica y evitar dispersión en desarrollo de software, se establecen las siguientes definiciones operativas formales:

> **Evaluación Adaptativa (Definición Operativa en 1 línea):**  
> *"Proceso analítico dinámico de re-evaluación del riesgo académico del estudiante ejecutado en etapas sucesivas (Momento 1: Admisión e Ingreso vs. Momento 2: Cierre del Primer Semestre), ajustando el pronóstico de permanencia conforme se consolida su rendimiento real."*

> **Personalización del Aprendizaje (Definición Operativa en 1 línea):**  
> *"Segmentación de la población estudiantil en perfiles multidimensionales homogéneos mediante aprendizaje no supervisado (Clustering), articulada con una matriz institucional de recomendaciones pedagógicas y tutoriales diferenciadas por nivel de riesgo."*

---

## 3. Delimitación Institucional y Empírica (Decisión D4)

* **Organización del Caso de Negocio:** Universidad Nacional Federico Villarreal (UNFV) – Facultad de Ingeniería Electrónica e Informática (FIEI). Se modela su estructura orgánica, sus 4 escuelas profesionales (Informática, Electrónica, Mecatrónica, Telecomunicaciones), su reglamento académico y su proceso de tutoría universitaria.
* **Dataset Empírico de Referencia (Benchmark):** Dataset abierto UCI Machine Learning (*Predict Students' Dropout and Academic Success*, 4,424 observaciones $\times$ 37 atributos). Se declara explícitamente como **prueba de concepto y validación analítica** de la arquitectura de datos y algoritmos de IA, ante la reserva de datos nominativos protegidos por la Ley de Protección de Datos Personales (Ley N° 29733).
* **Contexto Macroeconómico y Normativo:** Encuesta Nacional de Hogares (INEI ENAHO 2023, Módulos 300 y 500) y catálogo universitario nacional (TUNI / SUNEDU 2025-II). Se integran como información agregada de contexto laboral y estructural de la educación superior peruana.

---

## 4. Objetivos del Proyecto

### 4.1. Objetivo General
Diseñar e implementar una plataforma inteligente de gestión y análisis de datos basada en arquitectura de Business Intelligence (DataMart, ETL SSIS, Cubo OLAP SSAS y Dashboards Power BI) integrada con modelos de Machine Learning (Regresión Logística vs. Random Forest y Clustering), orientada a la evaluación adaptativa del riesgo académico y la recomendación personalizada de intervenciones institucionales para optimizar la retención estudiantil en la UNFV-FIEI.

### 4.2. Objetivos Específicos
1. **Modelar los procesos académicos AS-IS y TO-BE** de la FIEI-UNFV, identificando cuellos de botella en la detección del rezago y formalizando las preguntas de negocio y KPIs institucionales para la toma de decisiones gerenciales.
2. **Diseñar e implementar un DataMart dimensional bajo esquema estrella en SQL Server**, estructurando tablas de hechos y dimensiones conformadas con niveles rigurosos de granularidad y reglas de integridad referencial.
3. **Construir un flujo ETL automatizado mediante Visual Studio SQL Server Integration Services (SSIS)**, asegurando la extracción desde fuentes planas, perfilado, limpieza de calidad de datos, normalización vigesimal ($0\text{--}20$) y carga trazable al DataMart.
4. **Desarrollar y comparar modelos de Machine Learning supervisados y no supervisados en Python**, evaluando el desempeño comparativo de Regresión Logística y Random Forest en dos momentos temporales clave ($M_1$ y $M_2$) y segmentando perfiles estudiantiles para la personalización de intervenciones.
5. **Construir un Cubo OLAP multidimensional en SSAS y Dashboards ejecutivos en Power BI**, integrando las predicciones de IA con indicadores de gestión y un simulador interactivo de escenarios *What-If* para apoyar las decisiones de directores de escuela y tutores.

---

## 5. Matriz de Alcance: Lo que Incluye vs. Lo que NO Incluye

| Componente / Dimensión | Lo que SÍ Incluye el Proyecto (In-Scope) | Lo que NO Incluye (Out-of-Scope) | Justificación Metodológica |
|---|---|---|---|
| **Canal de Interacción** | Dashboards ejecutivos e interactivos en **Power BI Desktop** con parámetros What-If. | Desarrollo de plataformas Web Full-Stack, Apps móviles o microcápsulas frontend. | Power BI es la plataforma líder para modelado semántico dimensional, cómputo DAX y autoservicio analítico. Crear software transaccional web incrementa deuda técnica sin valor analítico incremental. |
| **Evaluación Pedagógica** | Evaluación adaptativa por hitos temporales ($M_1$: Ingreso, $M_2$: Semestre 1). | Tests adaptativos computarizados (CAT) basados en Teoría de Respuesta al Ítem (TRI) a nivel de preguntas/reactivos. | No existen datos de interacción reactivo por reactivo; forzarlo destruiría la trazabilidad del DataMart. |
| **Cruce de Datos** | Articulación conceptual y agregada por área académica / gestión entre UCI, TUNI y ENAHO. | Cruce forzado de estudiantes individuales entre UCI y ENAHO/TUNI mediante identificadores ficticios. | Divergencia de universos muestrales y unidades de análisis (microdatos académicos vs. encuestas probabilísticas). Un cruce sintético individual generaría falacia ecológica; se preserva la integridad de cada fuente. |
| **Pila Tecnológica** | SQL Server (DW), Visual Studio SSIS (ETL), SSAS (OLAP), Python Scikit-Learn (IA), Power BI. | Arquitecturas Data Lake Medallón complejas (Spark/Databricks) o bases NoSQL. | Alineación estricta con las herramientas exigidas por la cátedra en clase y la rúbrica. |
| **Población en Dashboard** | Predicciones de probabilidad calculadas para el 100% de la población (4,424 casos) mediante validación cruzada *out-of-fold*. | Predicción limitada únicamente al subconjunto de prueba (*test split*). | El *test split* se reserva para la validación algorítmica fuera de línea, pero la gestión tutorial requiere visibilidad del 100% de la cohorte matriculada para evitar puntos ciegos en la intervención temprana. |
| **Simulación What-If** | Modificación dinámica de umbrales de riesgo ($P(\text{Dropout})$) y porcentaje de cobertura tutorial en Power BI. | Promesas de reducción causal garantizada de deserción sin validación de campo. | La simulación modela escenarios de capacidad operativa institucional, manteniendo rigor ético y científico. |

---

## 6. Verificación de Criterios de Finalización (Fase A0)

- [x] **D1 cerrado:** Título oficial respetado íntegramente con subtítulo técnico de DataMart y ML.
- [x] **D2 cerrado:** Significado operativo de "adaptativa" definido formalmente (re-evaluación por etapas temporales $M_1$ y $M_2$).
- [x] **D3 cerrado:** Significado operativo de "personalización" definido formalmente (clustering en perfiles $\times$ matriz de intervenciones).
- [x] **D4 cerrado:** UNFV-FIEI como contexto del caso y dataset UCI como benchmark empírico justificado.
- [x] **Elevator pitch del equipo:** Cualquier integrante puede sustentar en 30 segundos el propósito exacto del sistema sin prometer componentes web ni inventar cruces de datos.
