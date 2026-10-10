# Guía del proyecto de evaluación adaptativa y aprendizaje personalizado

## Para qué sirve esta guía

Esta guía convierte la pauta del profesor en un plan que el equipo puede seguir. La idea es construir un prototipo que detecte señales de riesgo académico con datos disponibles, explique esas señales y sugiera apoyos de aprendizaje. El prototipo no debe etiquetar a una persona como “mal estudiante” ni tomar decisiones académicas por ella: debe ayudar a docentes y tutores a ofrecer apoyo a tiempo.

La pauta del curso pide una solución completa: entender el problema y sus usuarios, preparar los datos, diseñar un DataMart, cargarlo con ETL, construir KPI y análisis, entrenar y evaluar Machine Learning, conectar sus resultados al dashboard y proponer decisiones. El código de IA por sí solo no cumple el encargo.

## 1. Cómo aterrizar el tema del profesor

El tema asignado es **“Sistema Inteligente de Evaluación Adaptativa y Personalización del Aprendizaje Universitario”**. “Adaptativa” puede sonar a un sistema que cambia automáticamente la dificultad de cada pregunta. Para hacer eso de verdad, harían falta datos de respuestas pregunta por pregunta, tema de cada pregunta, nivel de dificultad y evidencia de dominio. El conjunto de datos que recomendamos para empezar no contiene todo eso.

Por eso, para este proyecto conviene definir la adaptación de una forma posible de demostrar:

> **El sistema actualiza la evaluación de progreso en distintos momentos del ciclo académico, estima la probabilidad de que el estudiante necesite apoyo y muestra una recomendación de seguimiento o práctica para que un docente/tutor la revise.**

Ejemplo: al inicio se calcula un perfil base usando antecedentes académicos no sensibles; al cierre del primer semestre se vuelve a calcular el riesgo usando el progreso académico observado. Si aparecen señales de poca aprobación o bajo rendimiento, el dashboard sugiere revisar el caso y ofrecer tutoría, práctica guiada o una evaluación diagnóstica. La recomendación es apoyo, no castigo ni una nota automática.

### Pregunta de investigación sugerida

**¿Puede un modelo de clasificación, usando información disponible al inicio y al cierre del primer semestre, identificar con suficiente anticipación a estudiantes que podrían necesitar apoyo académico y presentar ese resultado en un sistema BI que facilite acciones de acompañamiento?**

### Objetivo general sugerido

Diseñar e implementar un prototipo de analítica de aprendizaje que integre un DataMart, un proceso ETL, KPI, dashboard y un modelo de clasificación para estimar resultados académicos y apoyar recomendaciones de acompañamiento.

### Objetivos específicos sugeridos

1. Describir el proceso de evaluación y seguimiento académico que el prototipo busca apoyar.
2. Preparar y documentar un dataset abierto de educación superior, cuidando la privacidad y la calidad.
3. Diseñar e implementar un modelo dimensional para analizar progreso y resultados académicos.
4. Comparar al menos dos modelos de clasificación con métricas apropiadas.
5. Integrar resultados y recomendaciones en un dashboard de apoyo a decisiones.

### Qué sí y qué no promete el proyecto

**Sí:** estima riesgo en datos históricos, permite filtrar por programa/periodo/etapa, compara el resultado de modelos y propone apoyos revisables por una persona.

**No:** demuestra que una intervención vaya a mejorar las notas, reemplaza al docente, decide quién aprueba, adapta preguntas de examen en tiempo real ni predice con validez automática a estudiantes de la UNFV usando datos de una universidad de otro país. Para afirmar que una intervención mejora resultados haría falta realizar y evaluar una intervención educativa real.

## 2. Datos: qué usar y qué evitar

### Primera opción recomendada: el `data.csv` que ya está en la carpeta

En la carpeta principal del proyecto ya existe un `data.csv` cuya estructura coincide con el dataset **Predict Students’ Dropout and Academic Success** del repositorio UCI. La fuente describe 4,424 registros de educación superior y 36 variables de entrada; el resultado tiene tres categorías: abandono, continúa matriculado y egreso. Es una buena opción para un primer prototipo de clasificación y el repositorio indica licencia CC BY 4.0. Cítenlo y atribúyanlo como pide la licencia. [UCI: ficha y descarga del dataset](https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success)

Este dataset no es de la UNFV: fue creado con información de una institución portuguesa. En el informe, preséntenlo como un **caso académico de referencia** o una prueba de concepto; no digan que representa a los estudiantes peruanos ni a su universidad.

El target de tres clases es útil para el modelo. Para activar alertas, el dashboard puede mostrar la probabilidad de abandono y usar un umbral revisable por el equipo docente. “Continúa matriculado” no significa necesariamente que el estudiante haya culminado con éxito; mantengan las tres categorías separadas al analizar resultados.

**Cuidado con el momento de predicción:** el archivo contiene variables resumidas del primer y segundo semestre. Si dicen que predicen “temprano”, excluyan del modelo temprano las variables del segundo semestre y cualquier dato que solo se conoce después del momento en que se habría emitido la alerta. Pueden comparar dos escenarios: predicción al ingreso y actualización al cierre del primer semestre. Documenten exactamente qué columnas estaban disponibles en cada escenario.

### Alternativa más rica: OULAD

El **Open University Learning Analytics Dataset (OULAD)** es una fuente abierta y anonimizada sobre cursos, estudiantes, evaluaciones e interacciones en un entorno virtual de aprendizaje; la página oficial explica sus tablas relacionadas y ofrece la descarga en CSV. Permite estudiar actividad a través del tiempo, así que encaja mejor si quieren analizar participación semanal. Requiere más trabajo de integración y los archivos de interacción son grandes. [Página oficial de OULAD](https://research.stem.open.ac.uk/ouanalyse/dataset/) · [Artículo que describe OULAD](https://doi.org/10.1038/sdata.2017.171)

**Recomendación práctica:** empiecen con el `data.csv` ya disponible. Cambien a OULAD solo si el equipo quiere asumir la complejidad adicional y necesita actividad temporal del aula virtual. No mezclen ambos datasets: pertenecen a instituciones, periodos y estructuras diferentes.

### Datos peruanos

La Plataforma Nacional de Datos Abiertos y SUNEDU/TUNI pueden servir para dar contexto institucional agregado, por ejemplo oferta académica, instituciones o cantidades de matrícula. Eso puede apoyar un dashboard descriptivo de contexto, pero los datos agregados no sirven por sí solos para entrenar un modelo individual de riesgo porque no contienen un resultado académico individual vinculado. [Portal de Datos Abiertos del Perú, educación](https://www.datosabiertos.gob.pe/SEARCH/field_topic/educaci%C3%B3n-28)

En la carpeta también hay archivos institucionales relacionados con estudiantes. No los mezclen con el `data.csv` público ni publiquen filas, notas o identificadores. La ficha técnica de TUNI describe distintos tipos de información, incluidos datos a nivel de persona, y advierte que corresponde resguardar la confidencialidad. Para un proyecto de curso, es más seguro trabajar con el dataset público UCI. Si el profesor exige datos propios de la universidad, primero pidan autorización y una versión formalmente anonimizada; un identificador codificado también puede permitir reidentificar a alguien si se puede cruzar con otra fuente.

### Kaggle y datos simulados

Kaggle puede ser cómodo, pero muchas veces aloja una copia de UCI u OULAD. Busquen primero la fuente original para comprobar licencia, versión y atribución. Si usan Kaggle, citen también la fuente original y revisen si la copia fue modificada.

Los datos sintéticos sirven para probar el ETL, llenar tablas, demostrar filtros y crear perfiles ficticios para una captura de pantalla. **No sirven para afirmar que el modelo predice bien a estudiantes reales** si las etiquetas fueron inventadas por el equipo. Para los resultados de Machine Learning usen un dataset real, abierto y documentado; mantengan los registros sintéticos claramente separados.

## 3. Herramientas sugeridas

| Parte | Herramienta | Para qué la usarían |
|---|---|---|
| Exploración y preparación | Python en Jupyter Notebook o VS Code; pandas, numpy | Leer CSV, revisar columnas, calidad, distribuciones y preparar variables. |
| Machine Learning | Python; scikit-learn | Crear pipelines, entrenar y comparar clasificadores, calcular métricas y exportar predicciones. |
| Base analítica | SQL Server y SSMS | Crear staging, dimensiones, hechos, llaves, vistas y consultas SQL. |
| ETL | Python + SQL Server, o SSIS si lo tienen instalado | Extraer, limpiar/transformar y cargar. No es necesario usar SSIS si el grupo domina mejor SQL y Python. |
| OLAP y dashboard | Power BI Desktop; SSAS solo si el profesor pide un cubo formal | El modelo semántico de Power BI permite analizar la estrella con filtros, jerarquías y drill-down. Si la pauta o el profesor exige un cubo OLAP explícito, evalúen SQL Server Analysis Services y confirmen qué edición tienen disponible. |
| Diagramas | draw.io / diagrams.net | Proceso AS-IS/TO-BE, arquitectura ETL y estrella dimensional. |
| Documento | Word y gestor de referencias como Zotero | Redactar el paper y mantener citas APA. |

Mantengan los archivos ordenados, por ejemplo:

```text
proyecto/
  datos/raw/                 # copia original; no editar
  datos/processed/           # datos preparados para análisis
  notebooks/                 # exploración y modelos
  sql/                       # creación, carga y consultas
  dashboard/                 # archivo Power BI
  paper/                     # informe y figuras
  README.md                  # instrucciones y trazabilidad
```

## 4. Recorrido de implementación, paso a paso

### Paso 1: definir el proceso y la decisión

El proceso no es “usar IA”. Es **evaluar progreso y organizar apoyo académico**. Escriban quién usaría el sistema (docente, tutor, coordinación), cuándo revisaría la alerta y qué acción razonable podría tomar.

Preguntas de negocio que pueden guiar el diseño:

- ¿Qué proporción de estudiantes termina en cada categoría de resultado?
- ¿Cómo cambia el progreso según programa, cohorte o etapa académica?
- ¿Qué señales académicas tempranas se asocian con el resultado final?
- ¿Qué estudiantes simulados quedan en el grupo que conviene revisar primero?
- ¿Cuántos casos marcaría el sistema si se cambia el umbral de alerta?

No escriban “¿quiénes son malos estudiantes?” ni usen esa etiqueta en tablas o visualizaciones. El sistema identifica **casos para revisar y apoyar**, no personas culpables.

### Paso 2: guardar y documentar la fuente

1. Conserven `data.csv` original en `datos/raw/` sin modificarlo.
2. Registren fuente, fecha de descarga, licencia, número de registros/columnas, descripción del target y limitaciones.
3. Guarden un diccionario de datos: nombre de columna, significado, tipo, momento en que se conoce y si se usará o no.
4. Anoten una decisión por cada variable sensible o que pueda funcionar como proxy de una característica personal.

### Paso 3: explorar y revisar la calidad en Python

En un notebook, lean solo la fuente autorizada y revisen:

- cantidad de filas y columnas, tipos, categorías y proporción de cada resultado;
- valores nulos, filas duplicadas, valores imposibles y categorías raras;
- rangos y distribuciones de variables numéricas;
- qué variables se conocen al ingreso y cuáles aparecen al final del primer/segundo semestre;
- desbalance entre clases y posibilidad de sesgos.

No se queden con una limpieza automática: expliquen qué encontraron y qué decisión tomaron. La ficha UCI indica que el dataset no presenta valores faltantes, pero igual compruébenlo en su copia y validen duplicados/tipos. No impriman registros personales en el paper ni en las capturas.

### Paso 4: definir target, momento y variables

Una primera formulación viable es predecir las tres categorías finales de UCI. Construyan dos vistas del problema:

1. **Al ingreso:** usar únicamente datos disponibles al momento de matrícula/ingreso.
2. **Actualización después del primer semestre:** agregar solo indicadores del primer semestre ya ocurrido.

El segundo modelo representa mejor la parte adaptativa: el sistema vuelve a evaluar después de observar progreso. Excluyan variables del segundo semestre de ambos escenarios y no usen el target como variable de entrada. Si una columna describe algo que ocurre después de la predicción, también debe quedar fuera.

Consideren excluir género, nacionalidad, discapacidad, información económica u otros atributos sensibles del modelo principal. Si su uso está autorizado y tiene sentido académico, podrían analizarlos por separado para auditar si el error del modelo cambia entre grupos, sin usarlos para decidir apoyos individuales. Escriban esta decisión y su justificación.

### Paso 5: limpiar, transformar y preparar el conjunto para ML

En Python:

1. Separar `X` (variables de entrada) y `y` (resultado objetivo).
2. Convertir variables categóricas con `OneHotEncoder` y escalar las numéricas cuando el modelo lo necesite.
3. Poner imputación, codificación y modelo dentro de un `Pipeline` de scikit-learn. Ajustar el pipeline solo con entrenamiento para evitar fuga de información.
4. Dividir train/test con estratificación, por ejemplo 80/20 y semilla registrada. Si generan más de una fila temporal por estudiante, separar por estudiante para que sus snapshots no caigan a la vez en entrenamiento y prueba.
5. No aplicar oversampling/SMOTE antes de dividir train/test; si lo prueban, aplíquenlo solo dentro del entrenamiento.

Guarden la tabla preparada y las predicciones con nombres de columnas legibles. Scikit-learn documenta clasificación, validación y métricas; citen su documentación o el artículo de la herramienta en la metodología. [Scikit-learn, métricas de clasificación](https://scikit-learn.org/stable/modules/model_evaluation.html) · [Artículo de scikit-learn](https://www.jmlr.org/papers/v12/pedregosa11a.html)

### Paso 6: crear staging y DataMart en SQL Server

Primero carguen el archivo en una tabla de preparación, por ejemplo `stg_student_outcome`. No conviertan directamente un CSV crudo en el modelo final: staging conserva la entrada de la ETL y ayuda a revisar errores.

**Granularidad sugerida para el prototipo:** una fila por estudiante anónimo, programa/cohorte y etapa de evaluación (ingreso o cierre del primer semestre). Si mantienen solo un escenario, escriban claramente la granularidad elegida.

Un esquema estrella pequeño puede ser:

```text
DimPrograma       DimCohorte       DimEtapaEvaluacion
      \               |                 /
                 FactProgreso
               /      |       \
        DimResultado  DimFecha  (medidas académicas)
```

`FactProgreso` puede guardar unidades matriculadas/evaluadas/aprobadas y promedio de notas si existen en la fuente. Dimensiones candidatas: programa, cohorte/periodo, etapa de evaluación y resultado real. Usen claves sustitutas enteras para las dimensiones, como en el curso. No creen dimensiones para cada medida y no confundan variables de texto descriptivas con medidas numéricas.

Mantengan las predicciones aparte, por ejemplo en `FactPrediccion`, para guardar: etapa/fecha de cálculo, clase predicha, probabilidad por clase, modelo y versión. Como el archivo UCI no identifica personas mediante un identificador institucional, pueden asignar una clave técnica ficticia para el prototipo; no la presenten como código real de estudiante.

En el paper incluyan el diagrama del esquema estrella y una tabla con tabla, clave, atributos, medidas y granularidad. Si por tiempo deben reducir dimensiones, está bien: la coherencia del modelo importa más que la cantidad de tablas.

### Paso 7: documentar la ETL

El flujo completo será:

```text
CSV original
   → Python: validación, limpieza y variables derivadas
   → SQL Server: staging
   → SQL Server: carga de dimensiones
   → SQL Server: carga de hechos y controles de calidad
   → Python: entrenamiento y predicciones
   → SQL Server: tabla de predicciones
   → Power BI: KPI, alertas de revisión y recomendaciones
```

Pueden implementar la carga con pandas + `pyodbc`/SQLAlchemy, el asistente de importación de SSMS, T-SQL o SSIS. Registren filas recibidas, rechazadas y cargadas; controlen claves duplicadas, nulos, correspondencia de claves foráneas y conciliación de conteos. Para el proyecto alcanza con una carga reproducible y documentada; si automatizan recargas, expliquen el orden: primero dimensiones, luego hechos y predicciones.

### Paso 8: entrenar y comparar modelos

Comparen un modelo simple y explicable, como **regresión logística**, contra un modelo basado en árboles, como **Random Forest**. Ambos resuelven clasificación multiclase y permiten contrastar facilidad de explicación frente a capacidad de capturar relaciones no lineales. No elijan el ganador por intuición ni por accuracy solamente.

Reporten como mínimo:

- matriz de confusión;
- precision, recall y F1 por cada categoría;
- macro-F1 o balanced accuracy, además de accuracy;
- soporte, es decir, cuántos casos reales hay por clase.

Para su objetivo de apoyo, miren especialmente cuántos casos de abandono se les escapan (**recall de abandono**) y cuántas alertas de abandono son incorrectas (**precision de abandono**). Si muestran probabilidades, aclaren que son estimaciones, no certezas. Si cambian el umbral para alertar más casos, expliquen el costo de más falsas alarmas. [Guía de métricas de scikit-learn](https://scikit-learn.org/stable/modules/model_evaluation.html)

Usen explicación por importancia de variables o permutation importance como apoyo, no como prueba causal. “La variable está asociada con el resultado en este modelo” no significa “esa característica causa abandono”.

### Paso 9: convertir una predicción en una recomendación cuidadosa

Diseñen una pequeña matriz de decisión y valídenla con sentido pedagógico. Ejemplo inicial:

| Señal del sistema | Qué muestra | Acción de apoyo para revisar |
|---|---|---|
| Probabilidad elevada de abandono | El modelo estima mayor riesgo que el umbral acordado | Tutor/a revisa el caso; ofrecer contacto y preguntar qué apoyo necesita. |
| Muchas unidades matriculadas, pocas aprobadas | Brecha de progreso en el periodo | Sugerir tutoría académica y un plan de estudio manejable. |
| Resultado bajo en el primer semestre | El patrón indica que conviene revisar bases académicas | Ofrecer práctica guiada o evaluación diagnóstica por tema, si el curso dispone de esos contenidos. |
| Probabilidad intermedia | El resultado no es concluyente | Mostrar seguimiento, no emitir una alerta urgente automáticamente. |

Las reglas concretas deben basarse en columnas que realmente existen, ser revisadas por docente/tutor y aparecer como propuestas. El dataset UCI no contiene banco de preguntas ni correspondencia de cada nota con una competencia específica: por tanto, la parte de “personalización” será una recomendación de apoyo basada en patrones, no una adaptación automática de ejercicios por dominio de tema.

### Paso 10: implementar análisis OLAP y construir el dashboard

Conecten Power BI al DataMart en estrella y preparen relaciones, medidas y jerarquías para explorar los resultados por programa, cohorte, etapa y periodo. El usuario debe poder filtrar, cruzar y profundizar desde un resumen hasta una categoría más detallada (slice/dice y drill-down). Esto demuestra análisis multidimensional sobre el modelo de datos. Si el profesor exige un cubo OLAP de Analysis Services, agréguenlo solo después de confirmar disponibilidad/edición de SQL Server; no lo supongan como requisito instalado.

El dashboard debe contestar preguntas concretas. Páginas sugeridas:

1. **Resumen ejecutivo:** total de registros, distribución de resultados, porcentaje de alertas para revisión y filtros por programa/cohorte/etapa.
2. **Progreso académico:** aprobaciones/evaluaciones y promedio de progreso por programa y etapa.
3. **Predicción:** matriz de confusión o indicadores de validación; predicciones y probabilidades solo para perfiles anónimos/de demostración.
4. **Acciones:** lista priorizada para tutoría con categoría de apoyo sugerida, mostrando que es una recomendación a revisar.
5. **Escenario what-if opcional:** cambiar el umbral de alerta y observar cuántos casos se marcarían y cómo cambia precision/recall según el conjunto de prueba.

KPI posibles (ajusten sus fórmulas a la definición del dataset): proporción de egreso/abandono/continúa matriculado; tasa de aprobación de unidades; diferencia de progreso entre ingreso y cierre del primer semestre; número de alertas estimadas; recall y precision de la clase de abandono. No llamen “tasa de mejora” a una predicción: para medir mejora necesitarían observar una intervención y comparar resultados.

No pongan nombres, DNI, IDs reales, notas fila por fila ni atributos sensibles en Power BI o capturas del paper. Presenten agregados y registros anónimos de demostración.

## 5. Cómo escribir cada sección del paper

Sigan los capítulos que especifica el profesor. Agreguen subtítulos para que el lector entienda el trabajo; no hace falta cambiar el orden principal.

### Introducción

**En palabras simples:** cuenten qué problema están atendiendo, por qué importa y qué solución proponen. Delimiten el alcance desde el principio: prototipo académico entrenado con dataset público extranjero.

Incluyan contexto, problema, pregunta, objetivo general, objetivos específicos, importancia, alcance y limitaciones. Citen investigaciones sobre analítica de aprendizaje, predicción temprana y personalización en educación superior. Un diagrama sencillo de la solución puede cerrar esta sección.

### Capítulo I: Generalidades

**En palabras simples:** expliquen quién tendría el problema y cómo funciona hoy el seguimiento. Como no tienen autorización para presentar notas personales de su universidad, definan con honestidad una institución de referencia simulada o un proceso académico genérico. No inventen que entrevistaron a la universidad ni atribuyan a la UNFV cifras del dataset portugués.

Incluyan organización/área usuaria, proceso actual **AS-IS**, propuesta **TO-BE**, actores, entradas, decisiones y salida. Dibujen ambos procesos. Si no conocen datos internos, declárenlo como supuesto del prototipo.

### Capítulo II: Proyecto o tarea académica / marco teórico

**En palabras simples:** expliquen los conceptos necesarios para entender su diseño, citando fuentes confiables. No hagan una colección de definiciones copiadas; relacionen cada concepto con una decisión de su proyecto.

Subtemas de la pauta: BI; Data Warehouse/DataMart; datos, información y conocimiento; modelo dimensional, dimensiones, hechos, medidas, jerarquías y granularidad; OLAP; KPI; Machine Learning/IA. Añadan analítica de aprendizaje, evaluación adaptativa, personalización y privacidad/ética. Pueden incluir una tabla “concepto / explicación simple / cómo se usa aquí”.

### Capítulo III: Desarrollo de la solución

**En palabras simples:** aquí demuestran exactamente qué construyeron y cómo viajan los datos hasta la recomendación.

Orden recomendado:

1. **Requerimientos y preguntas de negocio:** tabla con usuario, pregunta, KPI y decisión que apoya.
2. **Fuente y calidad de datos:** procedencia, licencia, unidad de análisis, diccionario, limitaciones, control de calidad. Incluyan un diagrama de flujo o tabla de datos disponibles y excluidos.
3. **Modelo conceptual y base OLTP de referencia:** relaciones/entidades que necesitan para el problema. Si el dataset no tiene una base transaccional normalizada, expliquen que la entrada real es el archivo CSV y no inventen una OLTP que no recibieron.
4. **Granularidad y modelo dimensional:** declaren qué representa una fila y pongan modelo estrella con PK/FK.
5. **ETL e implementación SQL:** diagrama de extracción/transformación/carga, reglas, tablas y controles; incluyan extractos representativos de scripts en el cuerpo y el resto en anexos o repositorio.
6. **OLAP, KPI y dashboard:** capturas legibles, filtros y definiciones/fórmulas de KPI.
7. **Machine Learning:** objetivo, target, momento de predicción, columnas incluidas/excluidas, partición, preprocesamiento, modelos, métricas, limitaciones y explicación.
8. **Integración IA + BI:** describan dónde se almacenan probabilidades y cómo llegan al dashboard.
9. **Resultados y recomendaciones:** tabla de comparación de modelos, matriz de confusión, análisis de falsos negativos/positivos y acciones propuestas.

Las figuras y tablas recomendadas son: AS-IS/TO-BE, arquitectura ETL, esquema estrella, diccionario resumido, calidad de datos, matriz de confusión, tabla de métricas y dashboard. Numérenlas, pongan título y expliquen en el texto qué se debe mirar.

### Conclusiones

**En palabras simples:** respondan si cumplieron los objetivos y qué mostraron los datos y las métricas. No prometan que ya redujeron el abandono ni que el sistema sirve para toda universidad. La conclusión correcta puede ser que un modelo logró cierto resultado en el dataset público y que hace falta validación local.

### Sugerencias

**En palabras simples:** digan qué haría falta después: validar con datos locales anonimizados y autorización, probar recomendaciones con docentes, monitorear calidad/sesgo, conectar preguntas con temas si se quiere adaptación real, y evaluar si las tutorías cambian el resultado.

### Referencias bibliográficas

Usen APA de forma uniforme y citen cualquier definición, dato, método, dataset o imagen que no sea de ustedes. El profesor recomienda que 15–20 % de la bibliografía esté en inglés; como meta sencilla, incluyan al menos 3 o 4 fuentes académicas en inglés dentro de una bibliografía de unas 20 referencias. No cuentan URLs sueltas como artículos científicos.

## 6. Dónde buscar artículos y qué palabras poner

Busquen en Google Scholar, Scopus o Web of Science si la universidad tiene acceso; para fuentes abiertas, revisen ERIC, DOAJ, Springer, ACM/IEEE y repositorios institucionales. Usen una mezcla de español e inglés. Filtren por artículos revisados por pares, últimos 5–8 años para revisiones recientes y trabajos fundacionales para conceptos.

| Parte del paper | Qué tipo de fuente buscar | Palabras clave útiles |
|---|---|---|
| Introducción / problema | Revisiones o estudios de abandono, éxito académico y alertas tempranas | `student dropout prediction higher education early warning system`; `predicción temprana abandono universitario analítica de aprendizaje` |
| Capítulo I / proceso | Fuentes oficiales de la institución solo si describen hechos reales; literatura sobre acompañamiento/tutoría | `academic advising intervention higher education student success`; `tutoría universitaria acompañamiento académico` |
| Capítulo II / BI y DataMart | Libros/artículos de BI, DW, modelo dimensional y OLAP | `dimensional modeling data warehouse Kimball`; `business intelligence data mart OLAP higher education` |
| Capítulo II / KPI | Artículos sobre indicadores educativos y evaluación de progreso | `higher education student success indicators KPI learning analytics`; `indicadores de gestión educación superior KPI` |
| Capítulo II / IA educativa | Revisiones sobre analítica del aprendizaje, minería de datos educativa y personalización | `educational data mining learning analytics higher education systematic review`; `personalized adaptive learning higher education review` |
| Capítulo III / dataset y método | Artículo que describe el dataset, trabajos que lo usan, clasificación y métricas | `Predict Students Dropout Academic Success UCI Realinho`; `OULAD early prediction student performance`; `imbalanced multiclass classification macro F1 recall dropout` |
| Capítulo III / ética | Guías y estudios sobre privacidad, transparencia, sesgo y supervisión humana | `ethics learning analytics student privacy higher education`; `fairness bias student risk prediction human oversight` |

Fuentes verificadas para iniciar (lean el texto completo cuando esté disponible y elijan citas que de verdad usen):

1. Realinho, V., Martins, M. V., Machado, J., & Baptista, L. (2021). *Early Prediction of Student’s Performance in Higher Education: A Case Study*. En *Trends and Applications in Information Systems and Technologies* (pp. 166–175). [DOI: 10.1007/978-3-030-72657-7_16](https://doi.org/10.1007/978-3-030-72657-7_16). Es útil para describir el problema/dataset UCI y comparar el encuadre de predicción.
2. Kuzilek, J., Hlosta, M., & Zdrahal, Z. (2017). Open University Learning Analytics dataset. *Scientific Data, 4*, 170171. [DOI: 10.1038/sdata.2017.171](https://doi.org/10.1038/sdata.2017.171). Usen si eligen OULAD.
3. Larrabee Sønderlund, A., Hughes, E., & Smith, J. (2019). The efficacy of learning analytics interventions in higher education: A systematic review. *British Journal of Educational Technology, 50*, 2594–2618. [DOI: 10.1111/bjet.12720](https://doi.org/10.1111/bjet.12720). Sirve para hablar de por qué predecir no demuestra que una intervención funcione.
4. Ifenthaler, D., & Yau, J. Y.-K. (2020). Utilising learning analytics to support study success in higher education: A systematic review. *Educational Technology Research and Development, 68*, 1961–1990. [DOI: 10.1007/s11423-020-09788-z](https://doi.org/10.1007/s11423-020-09788-z).
5. du Plooy, E., Casteleijn, D., & Franzsen, D. (2024). Personalized adaptive learning in higher education: A scoping review of key characteristics and impact on academic performance and engagement. *Heliyon*. [DOI: 10.1016/j.heliyon.2024.e39630](https://doi.org/10.1016/j.heliyon.2024.e39630).
6. Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research, 12*, 2825–2830. [Artículo](https://www.jmlr.org/papers/v12/pedregosa11a.html). Fuente para justificar la herramienta de modelado, complementada por documentación técnica de métricas.
7. UNESCO. (2022). *Recommendation on the Ethics of Artificial Intelligence*. [Documento y resumen](https://www.unesco.org/en/articles/recommendation-ethics-artificial-intelligence). Útil para transparencia, equidad, gobernanza de datos y supervisión humana.

En la bibliografía final agreguen además fuentes académicas de Data Warehouse/modelamiento dimensional y KPI/Balanced Scorecard, priorizando los materiales y referencias de las clases cuando corresponda. No citen esta lista sin haber consultado el artículo y confirmado los datos APA exigidos por el profesor.

## 7. Qué figuras y tablas no deberían faltar

1. **Figura 1. Proceso actual AS-IS** y **Figura 2. Propuesta TO-BE**: quién hace qué y dónde se genera el apoyo.
2. **Figura 3. Arquitectura de solución**: fuente → Python/ETL → staging → DataMart → ML → dashboard → decisión.
3. **Figura 4. Esquema estrella**: hechos, dimensiones, claves y granularidad.
4. **Tabla 1. Diccionario de datos resumido**: target, variables candidatas, momento de disponibilidad y decisión de inclusión.
5. **Tabla 2. Calidad de datos**: regla, filas revisadas, hallazgo y corrección; reporten conteos, no registros individuales.
6. **Tabla 3. Comparación de modelos**: métricas por clase, macro-F1 y recall de abandono.
7. **Figura 5. Matriz de confusión**: muestre qué tipos de resultado se confunden.
8. **Figura 6. Dashboard**: captura con datos agregados o registros anónimos del dataset abierto.

Cada figura debe tener una idea. No llenen el paper de capturas de código; el SQL completo y notebooks pueden ir como anexos o archivos entregables.

## 8. Entregables del equipo y orden de trabajo

La pauta del profesor pide informe, dataset documentado, DataMart, scripts, ETL, modelo dimensional, OLAP/KPI, dashboard, notebook/código ML, dataset preparado, métricas, comparación/justificación, integración BI + IA y sustentación. Pueden organizar el trabajo así:

| Fase | Resultado que debe quedar guardado |
|---|---|
| 1. Definición | Problema, usuario, pregunta de investigación, objetivos, alcance y límites. |
| 2. Fuente | CSV original público, ficha de datos, licencia y diccionario. |
| 3. Análisis | Notebook EDA y reporte de calidad sin filas identificables. |
| 4. Diseño | AS-IS/TO-BE, arquitectura, granularidad, modelo lógico y diagrama estrella. |
| 5. ETL/SQL | Tablas staging, dimensiones, hechos, consultas de control y pasos de carga reproducibles. |
| 6. ML | Notebook con partición, pipelines, comparación, métricas y explicación de errores. |
| 7. BI | Dashboard Power BI con filtros, KPI, predicciones y acciones de apoyo. |
| 8. Paper | Capítulos completos, figuras/tablas citadas, APA y limitaciones honestas. |
| 9. Sustentación | Demostración desde el dato fuente hasta una decisión; explicar un falso positivo y un falso negativo. |

## 9. Checklist antes de entregar

- [ ] El problema describe una decisión concreta, no solo “usar inteligencia artificial”.
- [ ] Se declara que el dataset es público y extranjero, y se explica qué no permite concluir.
- [ ] Se especifica la granularidad y el momento en que se haría cada predicción.
- [ ] Se excluyeron variables futuras y se controló la fuga de datos.
- [ ] Se documentaron origen, licencia, limpieza, ETL, claves y conteos.
- [ ] El esquema estrella responde las preguntas de negocio.
- [ ] Se compararon al menos dos clasificadores con métricas por clase y matriz de confusión.
- [ ] El dashboard muestra resultados de IA junto a KPI, y no solo gráficos históricos.
- [ ] Las recomendaciones son de apoyo, revisables por una persona y no se presentan como causa comprobada.
- [ ] No aparecen nombres, identificadores, notas individuales ni datos internos prohibidos.
- [ ] Las conclusiones salen de los resultados medidos y no prometen efectos que no evaluaron.
- [ ] Las referencias están en APA y cumplen la proporción de fuentes en inglés recomendada.

## En resumen

Su idea sí va en la dirección del tema. Para volverla un proyecto claro, preséntenla como un **sistema de evaluación de progreso por etapas y alerta de apoyo académico**, con recomendaciones revisadas por docentes. Usen el `data.csv` público UCI para el primer modelo, implementen el flujo con Python + SQL Server + Power BI y reconozcan que la adaptación automática de preguntas requeriría otros datos. Así cubren el tema asignado y, a la vez, hacen afirmaciones que sus datos realmente pueden respaldar.
