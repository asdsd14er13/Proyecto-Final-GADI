# Cómo ejecutar el prototipo

Este avance llega hasta una comparación inicial de modelos de IA. Todavía no incluye paper ni Power BI. La fuente para entrenar es UCI; los archivos de TUNI quedan separados porque no contienen el resultado académico individual que necesita este modelo y uno de ellos incluye información personal.

## Archivos

- `notebooks/01_prototipo_analitica_adaptativa.ipynb`: flujo guiado desde lectura y revisión del CSV hasta preparación, entrenamiento, evaluación y exportación.
- `notebooks/01_prototipo_analitica_adaptativa.py`: mismo notebook en formato de celdas de Python, por si se trabaja en VS Code.
- `requirements.txt`: librerías necesarias.
- `sql/01_crear_datamart.sql`: crea staging, dimensiones y hechos en SQL Server.
- `sql/02_cargar_hecho.sql`: pasa el progreso desde staging a la tabla de hechos.
- `sql/03_cargar_predicciones.sql`: carga predicciones del conjunto de prueba.

## Orden recomendado

1. Abrir PowerShell en la carpeta del proyecto e instalar dependencias: `python -m pip install -r requirements.txt`.
2. Abrir el `.ipynb` en Jupyter Lab, Jupyter Notebook o VS Code y ejecutar las celdas en orden.
3. Revisar las métricas, la matriz de confusión y los CSV generados en `outputs/`.
4. En SSMS, crear una base de datos de práctica y ejecutar `sql/01_crear_datamart.sql`.
5. Importar `outputs/stg_progreso_uci.csv` a `stg.ProgresoUCI` y `outputs/predicciones_prueba.csv` a `stg.PrediccionesUCI` con el asistente de importación de SSMS. Confirmar que los encabezados coincidan con las columnas de las tablas.
6. Ejecutar `sql/02_cargar_hecho.sql` y luego `sql/03_cargar_predicciones.sql`.

Los identificadores `source_row_id` son números técnicos creados a partir del orden de filas de UCI. No son códigos personales. El archivo de staging tiene una fila por registro y momento de análisis (ingreso o cierre del primer semestre). Las predicciones guardadas son solo del conjunto de prueba para revisar el desempeño.

## Cómo interpretar la prueba

Se comparan regresión logística y Random Forest. La etiqueta tiene tres clases: `Dropout`, `Enrolled` y `Graduate`. En la corrida verificada, el mejor F1 macro al cierre del primer semestre fue aproximadamente 0.624; el recall de abandono quedó alrededor de 0.594. Son métricas de una sola partición de prueba y no demuestran validez en Perú. La clase `Enrolled` se confunde más que las otras, así que el resultado debe tratarse como prototipo y apoyo para revisión, no como decisión automática.

## Qué falta para una validación peruana

Se necesita una muestra institucional autorizada y seudonimizada que conecte, por estudiante y ciclo, información disponible en cada fecha con un resultado académico definido. Debe excluir identificadores directos y acordarse con la institución el uso de variables sensibles. El catálogo institucional TUNI puede aportar dimensiones descriptivas separadas, pero no debe mapearse a los códigos de programa de UCI sin equivalencias oficiales comprobadas.
