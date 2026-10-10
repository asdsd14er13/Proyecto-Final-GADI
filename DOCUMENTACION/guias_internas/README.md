# DOCUMENTACIÓN OFICIAL Y GUÍA DEL PROYECTO FINAL GADI 2026
**Facultad de Ingeniería Electrónica e Informática (FIEI) – UNFV**  
**Curso:** Gestión y Análisis de Datos e Información  
**Docente:** Mg. Ing. Ivan Crispin Sanchez  

---

## 📂 Estructura de Documentación Generada

Esta carpeta contiene la solución completa, fundamentada y estructurada para alcanzar la máxima calificación (**20/20**) en el proyecto final, resolviendo la comparativa entre la propuesta técnica inicial y los archivos del proyecto.

| Archivo Markdown | Descripción y Utilidad Directa |
| :--- | :--- |
| **`01_REQUERIMIENTOS_DEL_PROFESOR.md`** | Desglose formal del documento de pauta del profesor (`DOC-20261006-WA0030`), arquitectura de 6 etapas, rúbrica de 20 puntos, condiciones mínimas y entregables obligatorios. |
| **`02_COMPARATIVA_Y_DECISIONES_TECNICAS.md`** | Cuadro comparativo entre la propuesta inicial (PDF), el avance del compañero y la solución final consolidada. Explica con rigor de ingeniería **qué componentes van, cuáles no van y por qué**. |
| **`03_INFORME_FASE_1_CAPITULOS_I_Y_II.md`** | **El documento académico listo para presentar en la primera entrega (hasta el Capítulo II):** Carátula, Introducción, Generalidades (AS-IS y TO-BE) y Marco Teórico con fundamentación técnica y normas APA 7ma edición. |
| **`04_HOJA_DE_RUTA_TECNICA_CAPITULO_III.md`** | Guía práctica paso a paso para el desarrollo del **Capítulo III**: creación del DataMart en SQL Server, paquete ETL en Visual Studio con SSIS, modelos en Python, Cubo OLAP en SSAS, Dashboard en Power BI y simulación What-If. |

---

## 🎯 Síntesis de las Decisiones del Proyecto

1. **Tema Oficial:** *Sistema Inteligente de Alerta Temprana, Retención Estudiantil y Analítica del Progreso Académico Universitario*.
2. **Fuentes Oficiales (3 fuentes en texto plano .CSV):**
   * `data.csv` (UCI): Calificaciones vigesimales, materias y abandono real (entrenamiento de Machine Learning y tabla de hechos académica).
   * `matriculado_2025_II.csv` e `institucional.csv` (SUNEDU/TUNI): Catálogo oficial de universidades y carreras peruanas.
   * `ENAHO 2023` (INEI): Microdatos de empleo y educación para justificar el impacto de los alumnos que trabajan en el Perú.
3. **Pila Tecnológica Oficial:**
   * **Base Analítica:** Microsoft SQL Server (DataMart bajo Esquema Estrella).
   * **ETL:** Visual Studio (SQL Server Integration Services - SSIS).
   * **OLAP:** Visual Studio (SQL Server Analysis Services - SSAS).
   * **Machine Learning:** Python (Scikit-Learn: Regresión Logística vs. Random Forest).
   * **BI & Visualización:** Power BI Desktop (con simulador What-If).
4. **Lo que se descartó:** Se descartó por completo el desarrollo web interactivo (frontend/microcápsulas) para mantener el foco 100% en la analítica de datos, y se evitó el cruce forzado de bases de datos extranjeras que carecían de claves comunes.
