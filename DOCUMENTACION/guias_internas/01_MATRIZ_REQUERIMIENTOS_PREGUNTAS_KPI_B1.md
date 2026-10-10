# MATRIZ DE REQUERIMIENTOS, PREGUNTAS DE NEGOCIO Y CATÁLOGO DE KPIS (FASE B1)

**Curso:** Gestión y Análisis de Datos e Información (GADI) – 2026  
**Docente:** Mg. Ing. Ivan Crispin Sanchez  
**Institución:** Universidad Nacional Federico Villarreal (UNFV) – Facultad de Ingeniería Electrónica e Informática (FIEI)  
**Marco Metodológico:** Metodología Ralph Kimball (Planificación del Ciclo de Vida Dimensional) y Criterios 1, 2 y 4 de la Rúbrica Docente  
**Documento Fuente:** `05_PLAN_MAESTRO_DESARROLLO.md` (§3.B1 y §4.4)  
**Estado:** Formalizado y Validado (Hito B1 Completado)

---

## 1. Identificación y Mapeo de Actores del Negocio (Stakeholders)

Para que la solución de Business Intelligence e Inteligencia Artificial responda a problemas de gestión reales y no a reportes pasivos, se identifican 4 roles organizacionales clave dentro de la FIEI-UNFV:

| ID Actor | Rol Organizacional | Responsabilidad Funcional en el Proceso Académico | Nivel de Decisión |
| :---: | :--- | :--- | :---: |
| **ACT-01** | **Director de Escuela Profesional** (Informática / Electrónica / Mecatrónica / Telecomunicaciones) | Gestión curricular, programación académica, supervisión de tasas de matrícula, retención global por ciclo y asignación de presupuesto docente. | **Estratégico / Táctico** |
| **ACT-02** | **Comité de Tutoría y Consejería Universitaria (FIEI)** | Coordinación de planes de tutoría, monitoreo del semáforo de riesgo por cohorte, asignación de alumnos prioritarios a tutores y seguimiento de intervenciones. | **Táctico / Operativo** |
| **ACT-03** | **Docente Tutor / Consejero Académico** | Acompañamiento individual y grupal, diagnóstico pedagógico, asesoría personalizada en cursos troncales y derivación de casos críticos. | **Operativo** |
| **ACT-04** | **Oficina de Bienestar Universitario (UNFV/FIEI)** | Asignación de becas alimentarias, subsidios de pasaje, soporte psicopedagógico y programas de apoyo a estudiantes trabajadores o en vulnerabilidad económica. | **Táctico / Operativo** |

---

## 2. Historias de Necesidad de Información (User Stories Analíticas)

Siguiendo el estándar de ingeniería de requerimientos orientado a BI:

1. **US-01 (Director de Escuela):**  
   *Como* Director de Escuela Profesional,  
   *necesito* conocer la tasa global proyectada de deserción y el rendimiento promedio por cohorte y programa al cierre del primer semestre,  
   *para* reestructurar la oferta académica, planificar talleres extracurriculares de ciencias básicas y justificar recursos docentes ante el Decanato.
2. **US-02 (Comité de Tutoría):**  
   *Como* Presidente del Comité de Tutoría,  
   *necesito* identificar a los estudiantes en nivel de riesgo alto ($P(\text{Dropout}) \ge 0.60$) segmentados por factores de rezago antes de los exámenes parciales,  
   *para* priorizar la asignación de carga de tutoría individual y focalizar los horarios de asesoría.
3. **US-03 (Docente Tutor):**  
   *Como* Docente Consejero,  
   *necesito* visualizar el perfil individual del estudiante, sus antecedentes de admisión, asignaturas aprobadas en S1 y el perfil asignado por el modelo no supervisado (Clustering),  
   *para* prescribir una ruta de acompañamiento pedagógico pertinente y personalizada (tutoría de pares, nivelación matemática o refuerzo metodológico).
4. **US-04 (Bienestar Universitario):**  
   *Como* Trabajador Social de Bienestar Universitario,  
   *necesito* cruzar el nivel de riesgo predictivo con indicadores de vulnerabilidad socioeconómica (estudiantes becarios, deudores de tasas o con carga laboral excesiva),  
   *para* canalizar oportunamente becas comedor, apoyos económicos de emergencia y flexibilización horaria.
5. **US-05 (Director / Decano - Simulación):**  
   *Como* Autoridad Académica,  
   *necesito* simular escenarios interactivos modificando el umbral de corte del modelo de IA ($P_{\text{corte}}$) y la cobertura de intervención tutorial mediante un análisis *What-If*,  
   *para* proyectar el número de alumnos retenibles y optimizar la capacidad operativa de los tutores disponibles.

---

## 3. Catálogo Priorizado de Preguntas de Negocio

El sistema dimensional y el modelo predictivo se diseñan exclusivamente para dar respuesta verificable a las siguientes 8 preguntas de gestión:

| ID | Pregunta de Negocio | Perspectivas / Dimensiones Clave | KPI Asociado | Página Destino en Power BI |
| :---: | :--- | :--- | :--- | :--- |
| **PN-01** | ¿Cuál es la tasa de retención y deserción estudiantil histórica y cómo varía según el programa académico (escuela profesional)? | `DimPrograma`, `DimResultado`, `DimFuente` | KPI-01 (Tasa de Abandono Histórica) | 1. Visión Ejecutiva Institucional |
| **PN-02** | ¿Cómo evoluciona el rendimiento académico promedio entre la etapa de admisión ($M_1$) y el cierre del primer semestre ($M_2$)? | `DimEtapa`, `DimPrograma`, `DimEstudiante` | KPI-02 (Promedio Ponderado S1)<br>KPI-03 (Tasa de Eficiencia Curricular) | 2. Diagnóstico del Rendimiento |
| **PN-03** | ¿Cuántos estudiantes se encuentran en riesgo alto, medio y bajo según la predicción del modelo de Machine Learning en cada momento temporal? | `DimEtapa`, `DimNivelRiesgo`, `DimModelo` | KPI-04 (Volumen de Población en Riesgo Crítico) | 3. Semáforo Predictivo de IA |
| **PN-04** | ¿Cuál es la ganancia en precisión predictiva al re-evaluar al estudiante al final del primer semestre ($M_2$) en comparación con el ingreso ($M_1$)? | `DimEtapa`, `DimModelo`, `DimResultado` | KPI-05 (Sensibilidad / Recall del Modelo de Deserción)<br>KPI-06 (F1-Score Macro) | 3. Semáforo Predictivo de IA |
| **PN-05** | ¿Qué variables académicas y demográficas concentran la mayor importancia o peso en la probabilidad de abandono? | `DimPrograma`, `DimPerfil`, `DimEtapa` | KPI-07 (Importancia Relativa de Variables - SHAP/Gini) | 3. Semáforo Predictivo de IA |
| **PN-06** | ¿Cómo se distribuyen los estudiantes en los diferentes clústeres o perfiles socioacadémicos generados por aprendizaje no supervisado? | `DimPerfilCluster`, `DimNivelRiesgo` | KPI-08 (Distribución Poblacional por Perfil) | 4. Perfiles y Personalización |
| **PN-07** | ¿Qué paquete de intervención tutorial y pedagógica personalizada corresponde prescribir a cada perfil y nivel de riesgo? | `DimPerfilCluster`, `DimNivelRiesgo`, `DimIntervencion` | KPI-09 (Tasa de Asignación de Intervención) | 4. Perfiles y Personalización |
| **PN-08** | ¿Si el Comité de Tutoría interviene al $X\%$ de los estudiantes en riesgo con una efectividad supuesta del $Y\%$, cuántos abandonos se lograrían mitigar? | Parámetros What-If (`P_Umbral`, `Cobertura`, `Efectividad`) | KPI-10 (Estudiantes Proyectados Retenidos - What-If) | 5. Simulación de Escenarios (What-If) |

---

## 4. Fichas Técnicas del Catálogo de KPIs

### KPI-01: Tasa de Abandono Estudiantil Histórica (TDA)
* **Tipo:** Estratégico (Descriptivo histórico).
* **Fórmula Matemática:**  
  $$\text{TDA} = \frac{\sum \text{Estudiantes con Resultado = 'Dropout'}}{\sum \text{Total de Estudiantes Matriculados}} \times 100$$
* **Unidad de Medida:** Porcentaje ($\%$).
* **Meta Propuesta:** Mantener $\text{TDA} \le 18.0\%$ en primer ciclo (benchmark nacional SUNEDU).
* **Sentido:** Minimizar ($\downarrow$).
* **Columnas Requeridas:** `dw.FactProgreso.outcome_key`, `dw.DimResultado.outcome_code` ('Dropout', 'Enrolled', 'Graduate').

---

### KPI-02: Promedio de Calificación Curricular del Semestre 1 (PC-S1)
* **Tipo:** Táctico (Rendimiento académico).
* **Fórmula Matemática:**  
  $$\text{PC-S1} = \frac{\sum \text{curricular\_grade}}{\text{Conteo de Estudiantes con Calificación Registrada}}$$
* **Unidad de Medida:** Puntos en escala vigesimal ($0\text{ a }20$).
* **Meta Propuesta:** $\text{PC-S1} \ge 12.50$ puntos.
* **Sentido:** Maximizar ($\uparrow$).
* **Regla de Calidad:** Excluir registros donde $\text{curricular\_approved} = 0$ y $\text{curricular\_grade} = 0$ para evitar distorsión de abandono no evaluado (R11).
* **Columnas Requeridas:** `dw.FactProgreso.curricular_grade`, `stage_key = 'fin_primer_semestre'`.

---

### KPI-03: Tasa de Eficiencia Curricular en Semestre 1 (TEC-S1)
* **Tipo:** Táctico / Operativo.
* **Fórmula Matemática:**  
  $$\text{TEC-S1} = \frac{\sum \text{curricular\_approved}}{\sum \text{curricular\_enrolled}} \times 100$$
* **Unidad de Medida:** Porcentaje ($\%$).
* **Meta Propuesta:** $\text{TEC-S1} \ge 75.0\%$.
* **Sentido:** Maximizar ($\uparrow$).
* **Aditividad:** **No aditiva** (se calcula estrictamente como cociente de sumas en DAX/MDX, nunca promediando porcentajes).
* **Columnas Requeridas:** `dw.FactProgreso.curricular_approved`, `dw.FactProgreso.curricular_enrolled`.

---

### KPI-04: Volumen de Estudiantes en Riesgo Crítico (VRC)
* **Tipo:** Predictivo / Operativo (Generado por IA).
* **Fórmula Matemática:**  
  $$\text{VRC} = \sum_{i=1}^{N} \mathbb{I}\left(P_i(\text{Dropout}) \ge 0.60\right)$$
* **Unidad de Medida:** Número absoluto de estudiantes (Entero).
* **Meta Operativa:** $100\%$ de los estudiantes clasificados con intervención asignada en menos de 10 días hábiles.
* **Sentido:** Minimizar ($\downarrow$).
* **Columnas Requeridas:** `dw.FactPrediccion.prob_dropout`, `dw.FactPrediccion.stage_key`.

---

### KPI-05: Sensibilidad del Modelo de Abandono (Recall Dropout)
* **Tipo:** Técnico de Machine Learning (Calidad del Modelo).
* **Fórmula Matemática:**  
  $$\text{Recall}_{\text{Dropout}} = \frac{TP}{TP + FN}$$
  *Donde $TP$ = Verdaderos Positivos (Desertores reales detectados) y $FN$ = Falsos Negativos (Desertores reales que el modelo ignoró).*
* **Unidad de Medida:** Proporción ($0.00\text{ a }1.00$).
* **Meta Técnica:** $\text{Recall}_{\text{Dropout}} \ge 0.75$ en $M_2$ (Fin Semestre 1).
* **Justificación de Negocio:** En retención universitaria, un Falso Negativo (alumno en riesgo no detectado) cuesta la deserción definitiva del estudiante; por tanto, el Recall es la métrica de prioridad sobre el Precision general.
* **Columnas Requeridas:** `dw.FactPrediccion.predicted_outcome_key`, `dw.FactPrediccion.actual_outcome_key`.

---

### KPI-06: Valor Macro F1 Multiclase ($F_1\text{-Macro}$)
* **Tipo:** Técnico de Machine Learning.
* **Fórmula Matemática:**  
  $$F_1\text{-Macro} = \frac{1}{K} \sum_{k=1}^{K} 2 \times \frac{\text{Precision}_k \times \text{Recall}_k}{\text{Precision}_k + \text{Recall}_k} \quad (K=3)$$
* **Unidad de Medida:** Proporción ($0.00\text{ a }1.00$).
* **Meta Técnica:** $F_1\text{-Macro} \ge 0.65$ para superar la línea base ingenua frente a clases desbalanceadas (Graduate 49.9%, Dropout 32.1%, Enrolled 17.9%).
* **Sentido:** Maximizar ($\uparrow$).

---

### KPI-07: Índice de Cohesión de Perfiles de Aprendizaje (Coeficiente Silhouette)
* **Tipo:** Técnico de Clustering (Personalización).
* **Fórmula Matemática:**  
  $$s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))}, \quad \overline{S} = \frac{1}{N} \sum_{i=1}^N s(i)$$
* **Unidad de Medida:** Rango $[-1.00, +1.00]$.
* **Meta Técnica:** $\overline{S} \ge 0.35$ garantizando clústeres compactos y bien separados para personalización válida.

---

### KPI-08: Tasa de Retención Proyectada post Intervención (Simulador What-If)
* **Tipo:** Simulación Prescriptiva (What-If).
* **Fórmula Matemática:**  
  $$\Delta \text{Retenidos} = \sum_{i=1}^{N} \left[ \mathbb{I}(P_i(\text{Dropout}) \ge P_{\text{umbral}}) \times \text{Cobertura}_{\text{tut}} \times \text{Efectividad}_{\text{supuesta}} \right]$$
  $$\text{Tasa Retención Proyectada} = \frac{\text{Graduados/Matriculados Actuales} + \Delta \text{Retenidos}}{N_{\text{total}}} \times 100$$
* **Unidad de Medida:** Porcentaje ($\%$) y Conteo de Vidas Estudiantiles Salvadas.
* **Variables de Control Interactivas en Power BI:**
  * Parámetro 1: Umbral de Riesgo ($P_{\text{umbral}}$ de $0.30$ a $0.80$, paso $0.05$).
  * Parámetro 2: Cobertura Tutorial ($\% \text{ Cobertura}$ de $0\%$ a $100\%$, paso $10\%$).
  * Parámetro 3: Efectividad de la Intervención ($\% \text{ Éxito}$ de $0\%$ a $50\%$, paso $5\%$).

---

## 5. Matriz Integral de Trazabilidad: Actor ↔ Necesidad ↔ KPI ↔ Dimensión ↔ Decisión

| Actor | Necesidad de Negocio | Pregunta | KPI Concreto | Dimensiones del DataMart | Decisión de Gestión Habilitada |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **Director de Escuela** | Conocer el estado global de permanencia y carreras críticas. | PN-01 | KPI-01 (TDA) | `DimPrograma`, `DimResultado`, `DimFuente` | Asignar cupos de reforzamiento y balancear carga curricular. |
| **Director de Escuela** | Monitorear el progreso académico entre ingreso y primer ciclo. | PN-02 | KPI-02 (PC-S1)<br>KPI-03 (TEC-S1) | `DimEtapa`, `DimPrograma` | Evaluar pertinencia de cursos filtro (Cálculo, Algoritmos). |
| **Comité de Tutoría** | Identificar la lista nominal de casos críticos para asignar tutores. | PN-03 | KPI-04 (VRC) | `DimEstudiante`, `DimEtapa`, `DimNivelRiesgo` | Distribuir estudiantes en riesgo entre los docentes tutores disponibles. |
| **Comité de Tutoría** | Validar la confiabilidad de las alertas de la IA en cada ciclo. | PN-04 | KPI-05 (Recall)<br>KPI-06 (F1) | `DimModelo`, `DimEtapa` | Confiar en el semáforo predictivo y activar protocolos tempranos. |
| **Docente Tutor** | Comprender las causas raíces del bajo rendimiento individual. | PN-05 | KPI-07 (Importancia Variables) | `DimPerfilCluster`, `DimPrograma` | Orientar la conversación de tutoría a la causa real (académica o socioeconómica). |
| **Docente Tutor** | Brindar una intervención adaptada al perfil del alumno. | PN-06<br>PN-07 | KPI-08 (Distribución)<br>KPI-09 (Asignación) | `DimPerfilCluster`, `DimNivelRiesgo` | Prescribir tutoría de pares, nivelación en matemáticas o derivación. |
| **Bienestar Univ.** | Asignar becas y subsidios a estudiantes vulnerables en riesgo. | PN-03 | KPI-04 (VRC) | `DimPerfilCluster`, `DimNivelRiesgo` | Priorizar becas comedor y apoyo económico a estudiantes en riesgo alto. |
| **Autoridades FIEI** | Evaluar la viabilidad operativa de planes de tutoría masiva. | PN-08 | KPI-10 (What-If Retenidos) | Parámetros What-If en Power BI | Determinar cuántos tutores se necesitan contratar para salvar $X$ estudiantes. |

---

## 6. Perspectivas Dimensionales Identificadas (Insumo Directo para Kimball - Fase B3)

A partir de este catálogo de preguntas y KPIs, quedan formalizadas las **dimensiones analíticas del DataMart**:

1. **`DimEtapa` (Perspectiva Temporal del Sistema Adaptativo):**  
   Valores: *Momento 1 (Al ingreso / Admisión)* y *Momento 2 (Al cierre del primer semestre)*.
2. **`DimResultado` (Perspectiva de Condición Académica):**  
   Valores: *Graduate (Graduado)*, *Dropout (Desertor)*, *Enrolled (Matriculado/En curso)*.
3. **`DimPrograma` (Perspectiva Curricular):**  
   Valores: Escuelas profesionales de ingeniería y programas homologados CINE.
4. **`DimNivelRiesgo` (Perspectiva de Semáforo Predictivo):**  
   Valores: *Riesgo Bajo ($P < 0.40$)*, *Riesgo Medio ($0.40 \le P < 0.60$)*, *Riesgo Alto ($P \ge 0.60$)*.
5. **`DimModelo` (Perspectiva Algorítmica):**  
   Valores: *Regresión Logística (Línea Base)*, *Random Forest (Ensemble)*.
6. **`DimPerfilCluster` (Perspectiva de Personalización):**  
   Valores: Clústeres socioacadémicos generados por K-Means (Perfil A: Rendimiento Alto; Perfil B: Vulnerabilidad Académica; Perfil C: Sobrecarga Laboral).

---

## 7. Criterios de Finalización Superados (Fase B1)

- [x] **Actores mapeados:** Director de Escuela, Comité de Tutoría, Docente Tutor, Bienestar Universitario.
- [x] **8 preguntas de negocio definidas:** Cada una vinculada a un KPI, una dimensión y una pantalla de visualización.
- [x] **Fórmulas matemáticas rigurosas:** Ningún KPI ambiguo; aditividades explícitamente declaradas (TEC como no aditiva).
- [x] **Métricas de IA y What-If integradas:** Recall Dropout, F1 Macro, Silhouette y Retención Proyectada What-If formalizadas en el catálogo.
- [x] **Trazabilidad de datos:** 100% de los datos requeridos existen en las tablas verificadas del proyecto (`data.csv`, DataMart y salidas del modelo).
