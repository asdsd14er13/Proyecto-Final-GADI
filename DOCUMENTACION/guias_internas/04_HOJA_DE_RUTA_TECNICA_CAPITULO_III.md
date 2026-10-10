# 04. HOJA DE RUTA TÉCNICA Y GUÍA DE EJECUCIÓN (CAPÍTULO III)

**Fase:** Implementación Práctica, Código, ETL, Modelado y Dashboards  
**Propósito:** Guía paso a paso para ejecutar y verificar todos los entregables técnicos solicitados en el Capítulo III del profesor.

---

## 1. Mapa de Entregables del Capítulo III

```
CAPÍTULO III: DESARROLLO DE LA SOLUCIÓN
├── 1. Base de Datos & DataMart (SQL Server)
├── 2. Proceso ETL Automatizado (Visual Studio - SSIS)
├── 3. Módulo de Machine Learning (Python - Scikit-Learn)
├── 4. Cubo OLAP y Medidas Multidimensionales (Visual Studio - SSAS)
├── 5. Dashboard Inteligente (Power BI Desktop)
└── 6. Escenario de Simulación What-If (Reto Adicional)
```

---

## 2. Paso a Paso Detallado

### PASO 1: Creación del DataMart en SQL Server (SSMS)
1. Abre **SQL Server Management Studio (SSMS)** y conéctate a tu motor local.
2. Crea una base de datos nueva:
   ```sql
   CREATE DATABASE DM_RetencionEstudiantil;
   GO
   USE DM_RetencionEstudiantil;
   GO
   ```
3. Ejecuta el archivo que ya tienes en `sql/01_crear_datamart.sql`.
   * Esto creará los esquemas `stg` y `dw`, las tablas `stg.ProgresoUCI`, `stg.PrediccionesUCI`, las dimensiones `dw.DimEtapa`, `dw.DimResultado`, `dw.DimFuente`, y las tablas de hechos `dw.FactProgreso` y `dw.FactPrediccion`.
4. Ejecuta el script `sql/04_crear_datamart_matricula_tuni.sql` para tener listas las tablas institucionales peruanas (`dw.FactMatriculaTUNI`, `dw.DimInstitucionTUNI`, `dw.DimProgramaTUNI`, etc.).
5. **Captura obligatoria:** Ve a *Database Diagrams* en SSMS, agrega todas las tablas del esquema `dw` y toma una captura nítida del **Diagrama en Estrella**.

---

### PASO 2: Implementación del ETL con Visual Studio y SSIS
1. Abre **Visual Studio** con la extensión *SQL Server Integration Services Projects*.
2. Crea un proyecto nuevo: **Integration Services Project** con el nombre `ETL_RetencionEstudiantil`.
3. **Flujo de Control (`Package.dtsx`):**
   * **Tarea 1 (Execute SQL Task):** Limpieza de tablas de staging (`TRUNCATE TABLE stg.ProgresoUCI;`).
   * **Tarea 2 (Data Flow Task - Carga Progreso):**
     * **Origen:** *Flat File Source* apuntando a `data.csv` (delimitado por `;`).
     * **Transformación (Data Conversion):** Convertir cadenas y campos flotantes (`Curricular units 1st sem (grade)` a `DT_R8`).
     * **Transformación (Derived Column):** Validar que la nota esté en rango vigesimal ($0$ a $20$) y generar la columna `Condicion_Aprobado = (Curricular_grade >= 11.0) ? 1 : 0`.
     * **Destino:** *OLE DB Destination* mapeando directamente a `stg.ProgresoUCI`.
   * **Tarea 3 (Data Flow Task - Carga TUNI):**
     * Cargar el archivo procesado `outputs/stg_matricula_tuni.csv` a `stg.MatriculaTUNI`.
   * **Tarea 4 (Execute SQL Task - Poblar Hechos):**
     * Ejecutar el script `sql/02_cargar_hecho.sql` y `sql/05_cargar_matricula_tuni.sql`.
4. **Capturas obligatorias:** 
   * Captura del *Control Flow* con todas las tareas en verde.
   * Captura del *Data Flow* mostrando la cantidad de filas transferidas sin errores.

---

### PASO 3: Ejecución y Validación de Machine Learning en Python
1. Abre tu terminal o VS Code en la carpeta del proyecto.
2. Asegúrate de tener los paquetes instalados:
   ```powershell
   python -m pip install -r requirements.txt
   ```
3. Ejecuta el notebook `notebooks/01_prototipo_analitica_adaptativa.ipynb` (o el script `.py` correspondiente).
4. El notebook realizará:
   * Lectura de datos y separación de variables de entrada ($X$) y objetivo ($y$).
   * División estratificada Train/Test ($80/20$).
   * Entrenamiento de **Regresión Logística** vs. **Random Forest**.
   * Evaluación en dos momentos temporales: *Al Ingreso* y *Al Cierre del Primer Semestre*.
   * Cálculo de métricas: Balanced Accuracy, $F_1\text{-macro}$, Recall de Abandono y Matrices de Confusión.
5. Los resultados se guardarán automáticamente en la carpeta `outputs/`:
   * `outputs/comparacion_modelos.csv`
   * `outputs/predicciones_prueba.csv`
6. **Carga de Predicciones a SQL Server:**
   * Ejecuta el script `sql/03_cargar_predicciones.sql` para pasar las probabilidades generadas por Python hacia la tabla de hechos `dw.FactPrediccion`.
7. **Capturas obligatorias:** 
   * Tabla de métricas comparativas del notebook.
   * Gráfico de la Matriz de Confusión generado con `matplotlib`.

---

### PASO 4: Construcción del Cubo OLAP en SSAS (Visual Studio)
1. En Visual Studio, crea un proyecto de **Analysis Services Multidimensional and Data Mining Project** llamado `Cubo_RetencionEstudiantil`.
2. **Data Source:** Conecta a la base de datos `DM_RetencionEstudiantil` en SQL Server.
3. **Data Source View (DSV):** Agrega `FactProgreso`, `FactPrediccion`, `DimEtapa` y `DimResultado`.
4. **Diseño del Cubo:**
   * Medidas: Recuento de estudiantes, Suma de créditos aprobados, Promedio de calificación vigesimal.
   * Dimensiones: `DimEtapa` (Atributos: `Etapa`), `DimResultado` (Atributos: `Resultado`).
5. **Procesar y Desplegar:** Procesa el cubo y realiza una consulta de prueba en la pestaña *Browser*.
6. **Capturas obligatorias:** 
   * Estructura del cubo en Visual Studio.
   * Matriz de navegación multidimensional en el explorador del cubo.

---

### PASO 5: Dashboard Inteligente en Power BI Desktop
Conecta Power BI a SQL Server (importando las tablas `dw.FactProgreso`, `dw.FactPrediccion`, `dw.DimEtapa`, `dw.DimResultado` y `dw.FactMatriculaTUNI`).

Diseña **3 páginas estratégicas**:

#### Página 1: Diagnóstico Institucional y Contexto Laboral (BI Descriptivo)
* **Visual 1:** Tarjetas KPI con Total de Estudiantes, Tasa Histórica de Abandono y Promedio de Notas.
* **Visual 2:** Gráfico de barras de matrícula universitaria peruana por tipo de gestión (Pública vs. Privada) usando los datos TUNI.
* **Visual 3:** Gráfico descriptivo del perfil de trabajo y horas semanales de estudiantes (basado en ENAHO).

#### Página 2: Alerta Temprana y Semáforo de Riesgo (Integración BI + IA)
* **Visual 1 (Semáforo):** Gráfico circular o de barras clasificando a los alumnos según la probabilidad predicha por la IA:
  * 🔴 **Riesgo Alto:** Probabilidad de abandono $\ge 60\%$.
  * 🟡 **Riesgo Medio:** Probabilidad entre $40\%$ y $59\%$.
  * 🟢 **Riesgo Bajo:** Probabilidad $< 40\%$.
* **Visual 2 (Matriz Prescriptiva):** Tabla interactiva con columnas:
  * `ID Estudiante` | `Promedio 1er Ciclo` | `Probabilidad Abandono` | `Recomendación Sugerida`.
  * La recomendación se programa con una columna condicional en DAX:
    ```dax
    Recomendacion_Tutor = 
    IF(FactPrediccion[prob_dropout] >= 0.60, "Citación Urgente a Tutoría y Nivelación",
    IF(FactPrediccion[prob_dropout] >= 0.40, "Asignar Taller de Refuerzo Académico",
    "Seguimiento Ordinario"))
    ```

#### Página 3: Simulación What-If (Reto Adicional de la Rúbrica)
* En la pestaña **Modelado** de Power BI, haz clic en **Nuevo Parámetro $\to$ Campos numéricos**:
  * Nombre: `Umbral_Riesgo`
  * Mínimo: $0.30$, Máximo: $0.80$, Incremento: $0.05$, Valor predeterminado: $0.60$.
* Crea la Medida DAX reactiva:
  ```dax
  Alumnos_Para_Intervencion = 
  CALCULATE(
      COUNT(dw.FactPrediccion[source_row_id]),
      dw.FactPrediccion[prob_dropout] >= [Valor Umbral_Riesgo]
  )
  ```
* Crea una tarjeta y un gráfico que muestre cómo varía la cantidad de alumnos a intervenir y la demanda de horas de tutores docentes cuando el usuario desliza la barra del umbral.

---

### PASO 6: Preparación de la Sustentación y Defensa
El docente evaluará el **Criterio 8 (Sustentación y defensa - 2 puntos)** planteando escenarios empresariales como:  
* *"Si la deserción en primer ciclo sube un 15%, ¿qué información me da su sistema y qué decisiones recomiendan?"*

**Respuesta ganadora del grupo:**
1. Abrir la página del **Dashboard What-If en Power BI**.
2. Mostrar cómo ajustando el umbral de corte se detecta anticipadamente al cohorte de riesgo.
3. Argumentar con evidencia técnica: *"El modelo Random Forest detecta al 64.2% de los desertores reales antes de los exámenes parciales; la decisión inmediata es priorizar a los alumnos que trabajan más de 20 horas con notas menores a 11 para tutoría de nivelación y reprogramación de carga horaria."*
