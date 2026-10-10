# GUÍA OFICIAL PASO A PASO: MODELADO BPMN 2.0 EN BIZAGI MODELER
## PROYECTO: SISTEMA INTELIGENTE DE EVALUACIÓN ADAPTATIVA Y PERSONALIZACIÓN DEL APRENDIZAJE UNIVERSITARIO
**Institución:** Universidad Nacional Federico Villarreal (UNFV) — FIEI  
**Curso:** Gestión y Análisis de Datos e Información (GADI) 2026  
**Docente:** Mg. Ing. Ivan Crispin Sanchez  

---

## 1. INTRODUCCIÓN Y ACLARACIÓN METODOLÓGICA

En la metodología de modelado BPMN 2.0 (Business Process Model and Notation) enseñada en clase y utilizada en **Bizagi Modeler**, tanto el modelo **AS-IS** (situación actual) como el modelo **TO-BE** (situación futura propuesta) corresponden al **mismo proceso de negocio**:
> **Nombre del Proceso:** *Gestión de Seguimiento Académico, Alerta Temprana y Retención Estudiantil (Ciclo Regular de 16 Semanas)*.

* **El error común:** Modelar el TO-BE como un diagrama de arquitectura de software o capas de base de datos (ETL $\to$ Python $\to$ Power BI). En Bizagi eso es incorrecto, porque Bizagi modela **procesos de negocio organizacionales**, no tuberías de datos.
* **El enfoque correcto en Bizagi:** Ambos diagramas deben mostrar la interacción entre **participantes (Lanes)** a lo largo de las semanas del semestre (Semanas 0 a 16). En el **AS-IS**, las tareas son manuales, aisladas y tardías (provocando deserción); en el **TO-BE**, se incorpora el carril de la **Plataforma BI + IA**, que automatiza la ingesta, dispara alertas predictivas tempranas y prescribe intervenciones personalizadas para salvar al estudiante.

---

## 2. DIAGRAMA 1: MODELO AS-IS (SITUACIÓN ACTUAL)

### 2.1. Ficha del Diagrama
* **Nombre del Diagrama en Bizagi:** `Diagrama 1 - Proceso AS-IS`
* **Nombre del Pool (Contenedor):** `Proceso AS-IS: Seguimiento Académico Tradicional en FIEI-UNFV`
* **Carriles (Lanes) requeridos (3):**
  1. `Estudiante`
  2. `Docente de Asignatura`
  3. `Comité de Tutoría y Consejería`

---

### 2.2. Mapa de Elementos y Secuencia Paso a Paso (AS-IS)

#### CARRIL 1: `Estudiante`
1. **[Evento de Inicio]**
   * *Tipo en Bizagi:* Círculo simple verde (Start Event).
   * *Nombre:* `Inicio del Semestre Académico (Semana 0)`
2. **[Tarea 1]**
   * *Tipo en Bizagi:* Tarea de Usuario (👤 User Task - icono con persona).
   * *Nombre:* `Realizar matrícula regular en asignaturas`
   * *Conexión:* Flujo de secuencia desde el Evento de Inicio.
3. **[Tarea 2]**
   * *Tipo en Bizagi:* Tarea de Usuario (👤 User Task).
   * *Nombre:* `Asistir a clases y rendir prácticas (Semanas 1 a 7)`
   * *Conexión:* Flujo de secuencia desde Tarea 1.
4. **[Tarea 3]**
   * *Tipo en Bizagi:* Tarea de Usuario (👤 User Task).
   * *Nombre:* `Rendir Exámenes Parciales (Semana 8)`
   * *Conexión:* Flujo de secuencia desde Tarea 2.
5. **[Tarea 4]**
   * *Tipo en Bizagi:* Tarea de Usuario (👤 User Task).
   * *Nombre:* `Continuar ciclo en situación de incertidumbre`
   * *Conexión:* Flujo de secuencia desde Tarea 3.
6. **[Tarea 5]**
   * *Tipo en Bizagi:* Tarea de Usuario (👤 User Task).
   * *Nombre:* `Recibir citación tardía a tutoría (Semana 11-12)`
   * *Conexión:* Flujo de secuencia que viene desde la Lane del Comité de Tutoría.
7. **[Tarea 6]**
   * *Tipo en Bizagi:* Tarea de Usuario (👤 User Task).
   * *Nombre:* `Rendir Exámenes Finales (Semana 16)`
   * *Conexión:* Flujo de secuencia desde Tarea 4 (o tras la citación tardía).
8. **[Evento de Fin]**
   * *Tipo en Bizagi:* Círculo rojo de borde grueso (End Event).
   * *Nombre:* `Deserción o Repitencia Consumada (Pérdida de Gratuidad)`

---

#### CARRIL 2: `Docente de Asignatura`
9. **[Tarea 7]**
   * *Tipo en Bizagi:* Tarea Manual (✍️ Manual Task - icono con mano escribiendo).
   * *Nombre:* `Registrar notas de prácticas en Excel personal`
   * *Conexión:* Conectado tras rendir prácticas.
   * *Anotación de Texto (Rojo):* 
     > **[DOLOR 1: Silos de Información]**  
     > Las notas se quedan en laptops personales de los docentes. La facultad no tiene visibilidad del rendimiento durante 7 semanas.
10. **[Tarea 8]**
    * *Tipo en Bizagi:* Tarea Manual (✍️ Manual Task).
    * *Nombre:* `Calificar exámenes parciales físicos`
    * *Conexión:* Conectado tras rendir examen parcial.
11. **[Tarea 9]**
    * *Tipo en Bizagi:* Tarea de Usuario (👤 User Task).
    * *Nombre:* `Digitar calificaciones en la Intranet Docente (Semanas 9-10)`
    * *Conexión:* Flujo de secuencia desde Tarea 8.
    * *Anotación de Texto (Rojo):*
      > **[DOLOR 2: Latencia Informacional Crítica]**  
      > Retraso de hasta 10 semanas para centralizar las primeras notas oficiales. Imposible intervenir preventivamente.

---

#### CARRIL 3: `Comité de Tutoría y Consejería`
12. **[Tarea 10]**
    * *Tipo en Bizagi:* Tarea Manual / Usuario (👤 User Task).
    * *Nombre:* `Descargar y consolidar manualmente actas de intranet`
    * *Conexión:* Flujo de secuencia que recibe la notificación tras la carga de notas del docente.
    * *Anotación de Texto (Rojo):*
      > **[DOLOR 3: Diagnóstico Reactivo "Post-Mortem"]**  
      > Análisis manual en hojas de cálculo revisando promedios aritméticos simples una vez que el alumno ya jaló.
13. **[Compuerta Exclusiva 1]**
    * *Tipo en Bizagi:* Rombo con cruz interna ($\times$ Exclusive Gateway).
    * *Nombre:* `¿Promedio Parcial < 10.5?`
    * *Rama NO:* Flujo de secuencia que finaliza en `"Continuidad sin intervención"`.
    * *Rama SÍ:* Conecta a Tarea 11.
14. **[Tarea 11]**
    * *Tipo en Bizagi:* Tarea de Usuario (👤 User Task).
    * *Nombre:* `Emitir citación genérica a tutoría correctiva`
    * *Conexión:* Flujo de secuencia hacia el Estudiante (Tarea 5 en Carril 1).
    * *Anotación de Texto (Rojo):*
      > **[DOLOR 4: Intervención Uniforme y Tardía]**  
      > La citación llega en semana 11-12 con notas de 04 a 07 irrecuperables, sin diferenciar si el origen es económico, laboral o académico.

---

## 3. DIAGRAMA 2: MODELO TO-BE (SITUACIÓN PROPUESTA CON BI + IA)

### 3.1. Ficha del Diagrama
* **Nombre del Diagrama en Bizagi:** `Diagrama 2 - Proceso TO-BE`
* **Nombre del Pool (Contenedor):** `Proceso TO-BE: Sistema Inteligente de Evaluación Adaptativa y Personalización Académica`
* **Carriles (Lanes) requeridos (4):**
  1. `Estudiante`
  2. `Docente de Asignatura`
  3. `Plataforma Automatizada BI + IA (SSIS / SQL Server / Python / Power BI)`
  4. `Comité de Tutoría y Bienestar Universitario`

---

### 3.2. Mapa de Elementos y Secuencia Paso a Paso (TO-BE)

#### CARRIL 1: `Estudiante`
1. **[Evento de Inicio]**
   * *Tipo:* Círculo simple verde (Start Event).
   * *Nombre:* `Inicio de Semestre Académico (Semana 0)`
2. **[Tarea 1]**
   * *Tipo:* Tarea de Usuario (👤 User Task).
   * *Nombre:* `Registrar matrícula regular y completar ficha socioacadémica digital`
   * *Conexión:* Flujo de secuencia desde Inicio hacia el carril de la Plataforma BI+IA.
3. **[Tarea 2]**
   * *Tipo:* Tarea de Usuario (👤 User Task).
   * *Nombre:* `Asistir a clases y actividades del ciclo`
4. **[Tarea 3]**
   * *Tipo:* Tarea de Usuario (👤 User Task).
   * *Nombre:* `Participar activamente en el Plan de Intervención Personalizado asignado`
   * *Conexión:* Se activa al recibir la prescripción de tutoría/bienestar.
5. **[Tarea 4]**
   * *Tipo:* Tarea de Usuario (👤 User Task).
   * *Nombre:* `Rendir evaluaciones parciales y finales con soporte continuo`
6. **[Evento de Fin]**
   * *Tipo:* Círculo rojo de borde grueso (End Event).
   * *Nombre:* `Retención Estudiantil Exitosa y Continuidad Curricular`

---

#### CARRIL 2: `Docente de Asignatura`
7. **[Tarea 5]**
   * *Tipo:* Tarea de Usuario (👤 User Task).
   * *Nombre:* `Registrar calificaciones continuas en sistema institucional centralizado`
   * *Conexión:* Alimenta periódicamente el almacén de datos (sin silos en laptops).

---

#### CARRIL 3: `Plataforma Automatizada BI + IA`
8. **[Tarea 6]**
   * *Tipo:* Tarea de Servicio (⚙️ Service Task - icono con dos engranajes).
   * *Nombre:* `Ejecutar Pipeline ETL automatizado (Visual Studio SSIS)`
   * *Descripción:* Integra matrículas, trayectoria, catálogo y contexto ENAHO en el DataMart SQL Server.
9. **[Tarea 7]**
   * *Tipo:* Tarea de Servicio (⚙️ Service Task - ⚙️).
   * *Nombre:* `Calcular Probabilidad de Abandono - Momento 1: Ingreso (Python ML)`
   * *Descripción:* Ejecuta el modelo supervisado con variables de admisión en la Semana 2.
   * *Anotación de Texto (Verde):*
     > **[MEJORA 1: Detección Temprana en Semana 2]**  
     > Identifica estudiantes en riesgo 7 semanas antes del examen parcial, eliminando la latencia informacional.
10. **[Tarea 8]**
    * *Tipo:* Tarea de Servicio (⚙️ Service Task - ⚙️).
    * *Nombre:* `Segmentar estudiantes en Perfiles Socioacadémicos (K-Means Clustering)`
    * *Descripción:* Asigna el clúster (Vulnerable integral, Trabajador rezagado, Académico estricto).
    * *Anotación de Texto (Verde):*
      > **[MEJORA 2: Personalización por Clústeres]**  
      > La IA diagnostica la causa raíz del riesgo para prescribir la solución exacta según el perfil.
11. **[Tarea 9]**
    * *Tipo:* Tarea de Servicio (⚙️ Service Task - ⚙️).
    * *Nombre:* `Poblar dw.FactPrediccion y procesar Cubo OLAP (SSAS)`
12. **[Tarea 10]**
    * *Tipo:* Tarea de Servicio (⚙️ Service Task - ⚙️).
    * *Nombre:* `Re-evaluar Riesgo Dinámicamente - Momento 2: Cierre S1 / Parciales (Python ML)`
    * *Anotación de Texto (Verde):*
      > **[MEJORA 3: Evaluación Adaptativa en 2 Momentos]**  
      > Actualiza el nivel de riesgo comparando M1 (expectativa) vs M2 (rendimiento real).
13. **[Tarea 11]**
    * *Tipo:* Tarea de Envío / Servicio (⚙️ Service Task).
    * *Nombre:* `Publicar Dashboard Power BI y disparar alertas tempranas automáticas`
    * *Conexión:* Flujo de secuencia hacia el Carril del Comité de Tutoría.

---

#### CARRIL 4: `Comité de Tutoría y Bienestar Universitario`
14. **[Tarea 12]**
    * *Tipo:* Tarea de Usuario (👤 User Task).
    * *Nombre:* `Monitorear Semáforo Predictivo de Riesgo y Simular Escenarios What-If en Power BI`
    * *Anotación de Texto (Verde):*
      > **[MEJORA 4: Simulación y Decisión Basada en Datos]**  
      > Los directivos planifican la capacidad tutorial y optimizan recursos mediante simulación interactiva.
15. **[Compuerta Exclusiva 2]**
    * *Tipo:* Rombo con cruz interna ($\times$ Exclusive Gateway).
    * *Nombre:* `¿Riesgo Crítico (P >= 60%)?`
    * *Rama NO:* Acompañamiento regular preventivo.
    * *Rama SÍ:* Conecta a Tarea 13.
16. **[Tarea 13]**
    * *Tipo:* Tarea de Regla de Negocio (📋 Business Rule Task - icono con tabla/matriz).
    * *Nombre:* `Prescribir Intervención Focalizada según Matriz de Recomendación`
    * *Sub-acciones según Clúster:*
      * *Clúster Académico:* Taller de nivelación en Cálculo/Física y tutoría de pares.
      * *Clúster Laboral:* Flexibilidad horaria y soporte asincrónico.
      * *Clúster Vulnerable:* Priorización en Beca Comedor y subsidio de Bienestar.
17. **[Tarea 14]**
    * *Tipo:* Tarea de Usuario (👤 User Task).
    * *Nombre:* `Asignar y ejecutar tutoría personalizada con el Estudiante`
    * *Conexión:* Flujo de secuencia hacia el Estudiante (Tarea 3 en Carril 1).

---

## 4. GUÍA PRÁCTICA PARA CONSTRUIRLO EN BIZAGI MODELER (CLICK A CLICK)

Si abres **Bizagi Modeler**, sigue estos pasos exactos:

### Paso 1: Configurar la Hoja de Trabajo
1. Abre Bizagi Modeler $\to$ Nuevo Modelo.
2. En la paleta izquierda, haz clic en **Pool** (el icono de rectángulo grande) y arrástralo al lienzo.
3. Haz doble clic en el encabezado izquierdo del Pool y escribe el título del proceso.

### Paso 2: Crear los Carriles (Lanes)
1. En la paleta izquierda, selecciona **Lane** y arrástralo dentro del Pool.
2. Repite hasta tener los 3 carriles para el AS-IS (o 4 carriles para el TO-BE).
3. Haz doble clic en cada etiqueta de carril y escribe los nombres indicados arriba.

### Paso 3: Agregar Actividades y Cambiarles el Tipo de Tarea
1. Arrastra el **Evento de Inicio** (círculo verde) al primer carril (`Estudiante`).
2. Haz clic en la flecha rápida que sale del círculo verde para crear una **Tarea** (rectángulo redondeado).
3. Escribe el nombre de la tarea.
4. **Para cambiar el tipo de tarea en Bizagi:**
   * Haz clic derecho sobre la tarea $\to$ selecciona **Tipo de Tarea (Task Type)**.
   * Selecciona:
     * **Tarea de Usuario (User Task 👤)**: Para actividades humanas frente al computador.
     * **Tarea Manual (Manual Task ✍️)**: Para actividades en papel o registros manuales.
     * **Tarea de Servicio (Service Task ⚙️)**: Para scripts automáticos (ETL, Python, SSAS).
     * **Tarea de Regla de Negocio (Business Rule Task 📋)**: Para la asignación de recomendaciones según perfil.

### Paso 4: Agregar Compuertas Exclusivas
1. Arrastra una **Compuerta** (rombo) al lienzo.
2. Clic derecho $\to$ **Tipo de Compuerta $\to$ Exclusiva (Exclusive Gateway $\times$)**.
3. Nombra la compuerta con la pregunta (ej: `¿Riesgo >= 60%?`).
4. Conecta las dos salidas (una flecha etiquetada `"Sí"` y otra `"No"`).

### Paso 5: Agregar las Anotaciones de Dolor (Rojo) y Mejora (Verde)
1. En la paleta izquierda, sección **Artefactos**, selecciona **Anotación (Text Annotation)** (parece un corchete `[` con texto).
2. Arrástralo cerca de la tarea correspondiente.
3. Copia y pega el texto del dolor o mejora indicado en esta guía.
4. Conecta la anotación a la tarea usando el conector de **Asociación** (línea discontinua).
5. *(Opcional en Bizagi):* Puedes cambiar el color de relleno de la anotación a rojo suave para dolores y verde suave para mejoras.

### Paso 6: Exportar la Imagen para el Informe
1. En el menú superior de Bizagi, ve a la pestaña **Publicar** o **Exportar**.
2. Haz clic en **Imagen (Image)** $\to$ Formato **PNG** o **JPEG** (Resolución alta: 300 DPI).
3. Guarda las imágenes en tu carpeta:
   * `DOCUMENTACION/imagenes/diagrama_bpmn_as_is.png`
   * `DOCUMENTACION/imagenes/diagrama_bpmn_to_be.png`

---

## 5. COMPARACIÓN RÁPIDA DE ELEMENTOS BPMN EN BIZAGI

| Elemento BPMN | Icono en Bizagi | Uso en AS-IS | Uso en TO-BE |
| :--- | :---: | :--- | :--- |
| **Start Event** | 🟢 Círculo verde fino | Inicio de semestre | Inicio de semestre |
| **User Task** | 👤 Rectángulo con persona | Matrícula, digitar notas | Matrícula digital, monitoreo Power BI |
| **Manual Task** | ✍️ Rectángulo con mano | Notas en Excel personal, exámenes físicos | *(No se usa; todo está digitalizado)* |
| **Service Task** | ⚙️ Rectángulo con engranajes | *(No existe; todo es manual)* | SSIS ETL, Modelos Python ML, Cubo SSAS |
| **Business Rule Task** | 📋 Rectángulo con matriz | *(No existe; criterios arbitrarios)* | Matriz de prescripción según clúster IA |
| **Exclusive Gateway** | ❌ Rombo con cruz | ¿Promedio < 10.5? (Semana 10) | ¿Riesgo predictivo $\ge 60\%$? (Semana 2) |
| **End Event** | 🔴 Círculo rojo grueso | Deserción / Pérdida de gratuidad | Retención estudiantil y éxito académico |
| **Anotación** | `[` Corchete con texto | 4 Puntos de Dolor (Rojos) | 4 Mejoras Estratégicas (Verdes) |
