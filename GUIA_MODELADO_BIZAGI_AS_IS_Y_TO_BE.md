# 📋 MANUAL DE ENCARGO: MODELADO DE PROCESOS AS-IS Y TO-BE EN BIZAGI
**Proyecto:** Sistema Inteligente de Evaluación Adaptativa y Personalización del Aprendizaje Universitario  
**Institución:** Universidad Nacional Federico Villarreal (UNFV) — FIEI  
**Destinatario:** Miembro del Equipo de Desarrollo / Modelador BPMN  
**Entregables requeridos:** 
1. Archivo nativo `.bpm` de Bizagi Process Modeler con los dos diagramas.
2. Dos imágenes exportadas en alta resolución (`AS_IS_BPMN.png` y `TO_BE_BPMN.png`, 300 DPI) para el informe en Word.

---

## 🎯 OBJETIVO DEL ENCARGO
Modelar con precisión formal BPMN 2.0 en Bizagi los dos procesos del proyecto descritos en el **Capítulo I** de nuestro informe:
* **Diagrama 1 (AS-IS):** Proceso actual tradicional (manual, reactivo, con silos en Excel y latencia de 10 semanas).
* **Diagrama 2 (TO-BE):** Proceso futuro optimizado con Business Intelligence y Machine Learning (automatizado, preventivo en 2 hitos $M_1$ y $M_2$).

---

## ⚙️ CONFIGURACIÓN INICIAL EN BIZAGI MODELER
1. Abre **Bizagi Process Modeler**.
2. Ve a la pestaña inferior de diagramas y renombra:
   * Pestaña 1: `1. Proceso Actual (AS-IS)`
   * Pestaña 2: `2. Proceso Futuro (TO-BE)` *(usa el botón "+" para agregar nuevo diagrama)*.
3. **Regla de estilo visual:**
   * Tipografía: **Segoe UI** o **Arial**, tamaño 8 o 9 pt (legible y estético).
   * Líneas de flujo: Ortogonales (rectas en ángulo de 90°), sin cruces innecesarios.
   * Asignar a cada tarea su **Tipo de Tarea (Task Type)** haciendo clic derecho $\rightarrow$ *Task Type*.

---

# 📌 DIAGRAMA 1: PROCESO ACTUAL (AS-IS)
> *Muestra cómo la facultad gestiona actualmente el seguimiento: tarde, en papel, con Excel aislados y sin saber por qué reprueba el alumno.*

### 1. Estructura de Contenedores
* **1 Pool (Piscina):** `PROCESO DE SEGUIMIENTO ACADÉMICO Y RETENCIÓN ESTUDIANTIL (AS-IS)`
* **3 Carriles (Lanes) horizontales:**
  1. `Estudiante FIEI` (superior)
  2. `Docente de Asignatura` (intermedio)
  3. `Comité de Tutoría` (inferior)

### 2. Inventario de Elementos y Textos Exactos

| N° | Carril | Elemento BPMN | Texto / Nombre Exacto | Tipo de Tarea / Detalle |
| :---: | :--- | :--- | :--- | :--- |
| **0** | Estudiante | Start Event (Círculo verde) | `Inicio del Semestre Académico` | Evento de inicio simple |
| **1** | Estudiante | User Task (Persona) | `1. Realizar matrícula regular (Semana 0)` | Asociar objeto de datos: `Ficha de matrícula básica` |
| **2** | Estudiante | User Task (Persona) | `2. Asistir a clases y rendir evaluaciones continuas (Sem. 1-7)` | Conecta con la tarea 3 del docente |
| **3** | Docente | Manual Task (Mano) | `3. Registrar calificaciones en hojas locales (Sem. 1-7)` | Asociar objeto de datos: `Excel personal en laptop` |
| **4** | Estudiante | User Task (Persona) | `4. Rendir exámenes parciales (Semana 8)` | Conecta con tarea 5 |
| **5** | Docente | User Task (Persona) | `5. Calificar pruebas y digitar notas en intranet (Sem. 9-10)` | Asociar objeto de datos: `Acta parcial en intranet` |
| **6** | Comité Tutoría | User Task (Persona) | `6. Revisar actas y filtrar promedios < 10.5 manualmente (Sem. 10-11)` | Conecta a compuerta XOR |
| **G1** | Comité Tutoría | Exclusive Gateway (Rombo X) | `¿Estudiante con promedio < 10.5?` | Compuerta de decisión |
| **7** | Comité Tutoría | Manual Task (Mano) | `7. Emitir y enviar citación genérica en papel/correo (Sem. 11-12)` | Rama "SÍ" de la compuerta. Asociar datos: `Padrón impreso` |
| **8** | Estudiante | User Task (Persona) | `8. Asistir a sesión de tutoría tardía (Semana 12)` | Recibe la citación de la tarea 7 |
| **9** | Estudiante | User Task (Persona) | `9. Rendir exámenes finales (Semana 16)` | Recibe flujo de tarea 8 y de rama "NO" de compuerta G1 |
| **10** | Docente | User Task (Persona) | `10. Digitar y cerrar actas finales del ciclo (Semana 16)` | Cierre oficial de notas |
| **Fin**| Docente | End Event (Círculo rojo) | `Cierre de ciclo con reprobación, rezago y pérdida de gratuidad` | Evento de fin |

### 3. Anotaciones Obligatorias de "Dolores de Gestión" (Callouts en Rojo)
*En Bizagi, arrastra el icono de **Anotación** (corchete `[`), ponle relleno rojo claro (`#FEE2E2`) y conéctalo con línea punteada a la tarea señalada:*
1. **Conectado a Tarea 3 (Docente):**  
   `⚡ DOLOR 1 (Silos de Información): Notas en computadoras docentes; facultad a oscuras las primeras 7 semanas.`
2. **Conectado a Tarea 5 (Docente):**  
   `⚡ DOLOR 2 (Latencia Crítica): Retraso de 9 a 10 semanas para disponer de notas consolidadas en el sistema.`
3. **Conectado a Tarea 6 (Tutoría):**  
   `⚡ DOLOR 3 (Detección Post-Mortem): Diagnóstico reactivo con promedio simple (< 10.5) cuando el daño ya ocurrió.`
4. **Conectado a Tarea 7 (Tutoría):**  
   `⚡ DOLOR 4 (Intervención Uniforme): Citación genérica sin distinguir causa (laboral, matemática o económica).`

---

# 📌 DIAGRAMA 2: PROCESO FUTURO OPTIMIZADO (TO-BE)
> *Muestra la solución con Inteligencia de Negocios e IA: carril automatizado, predicción temprana M1, reevaluación adaptativa M2 y simulación What-If.*

### 1. Estructura de Contenedores
* **1 Pool (Piscina):** `PROCESO INTELIGENTE DE SEGUIMIENTO ADAPTATIVO Y RETENCIÓN ESTUDIANTIL CON BI + IA (TO-BE)`
* **4 Carriles (Lanes) horizontales:**
  1. `Estudiante FIEI`
  2. `Docente de Asignatura / Docente Tutor`
  3. `Dirección de Orientación y Tutoría (Comité / Directores)`
  4. `Plataforma Analítica Automatizada (BI + IA)` *(¡Nuevo carril tecnológico!)*

### 2. Inventario de Elementos y Textos Exactos

| N° | Carril | Elemento BPMN | Texto / Nombre Exacto | Tipo de Tarea / Detalle |
| :---: | :--- | :--- | :--- | :--- |
| **0** | Estudiante | Start Event (Círculo verde) | `Apertura de Proceso de Matrícula` | Evento de inicio |
| **1** | Estudiante | User Task (Persona) | `1. Realizar matrícula web y completar ficha socioacadémica (Sem. 0)` | Objeto de datos: `Ficha socioacadémica (horas trabajo, contexto)` |
| **2** | Plataforma BI+IA | Service Task (Engranajes) | `2. Ejecutar pipeline ETL SSIS: extracción y validación de calidad (Sem. 1)` | Almacén de datos (Data Store): `DataMart dw (SQL Server)` |
| **3** | Plataforma BI+IA | Script Task (Código/Engranaje) | `3. Procesar modelo predictivo M1 en Python (Random Forest + K-Means) (Sem. 1-2)` | Calcula $P(\text{Drop}) M_1$ y segmenta en clústeres |
| **G1** | Plataforma BI+IA | Exclusive Gateway (Rombo X) | `¿Riesgo M1 detectado? [P(Drop) >= 0.5]` | Decisión automática |
| **4** | Dir. Tutoría | User Task (Persona) | `4. Consultar Dashboard Power BI y prescribir plan diferenciado (Sem. 2-3)` | Objeto de datos: `Semáforo de riesgo y ficha individual Power BI` |
| **5** | Estudiante | User Task (Persona) | `5. Recibir notificación temprana y plan de acompañamiento personalizado (Sem. 3)` | Recibe plan según clúster (nivelación, beca o flexibilidad) |
| **6** | Estudiante | User Task (Persona) | `6. Asistir a clases y rendir evaluaciones continuas (Sem. 4-8)` | Trayectoria académica activa |
| **7** | Docente | User Task (Persona) | `7. Registrar notas de prácticas en intranet centralizada en vivo (Sem. 4-8)` | ¡Cero silos en laptops! Alimenta directamente el sistema |
| **8** | Plataforma BI+IA | Service Task (Engranajes) | `8. Re-evaluación adaptativa M2: procesar Cubo SSAS y varianza Delta P (Sem. 9-10)` | Recalcula riesgo con notas de mitad de ciclo |
| **G2** | Plataforma BI+IA | Exclusive Gateway (Rombo X) | `¿Evolución en M2?` | Bifurcación: Recuperado ($\Delta P < 0$) vs Crítico ($\Delta P \ge 0$) |
| **9** | Dir. Tutoría | User Task (Persona) | `9. Ejecutar simulación What-If en Power BI y redistribuir tutores (Sem. 11-14)` | Ajuste de umbral de riesgo y capacidad docente |
| **10**| Docente Tutor | User Task (Persona) | `10. Impartir asesorías focalizadas y monitorías de rescate (Sem. 11-15)` | Tutoría especializada orientada a la causa raíz |
| **11**| Estudiante | User Task (Persona) | `11. Rendir evaluaciones finales con soporte efectivo (Semana 16)` | Evaluaciones de fin de ciclo |
| **12**| Dir. Tutoría | User Task (Persona) | `12. Auditar retención de cohorte y generar reporte SINEACE/SUNEDU (Sem. 16)` | Objeto de datos: `Informe ejecutivo de retención auditado` |
| **Fin**| Dir. Tutoría | End Event (Círculo rojo) | `Cohorte culminada: Retención maximizada y gratuidad preservada` | Evento de fin exitoso |

### 3. Anotaciones de "Valor Agregado BI + IA" (Callouts en Verde)
*En Bizagi, arrastra **Anotaciones** con relleno verde claro (`#DCFCE7`) y conéctalas a:*
1. **Conectado a Tarea 3 (Plataforma):**  
   `✓ VALOR AGREGADO 1: Detección preventiva en Semana 2 al ingreso, sin esperar a desaprobar parciales.`
2. **Conectado a Tarea 4 (Tutoría):**  
   `✓ VALOR AGREGADO 2: Prescripción personalizada por Clúster (Académico, Laboral o Económico).`
3. **Conectado a Tarea 7 (Docente):**  
   `✓ VALOR AGREGADO 3: Erradicación de silos locales; 100% de notas centralizadas en el DataMart.`
4. **Conectado a Tarea 8 (Plataforma):**  
   `✓ VALOR AGREGADO 4: Evaluación adaptativa dinámica (M1 vs M2) con seguimiento de trayectoria Delta P.`
5. **Conectado a Tarea 9 (Tutoría):**  
   `✓ VALOR AGREGADO 5: Simulación interactiva What-If para optimizar la capacidad institucional.`

---

## 🎨 GUÍA DE COLORES Y ESTILO PARA BIZAGI
Para que los diagramas tengan calidad ejecutiva universitaria:
* **Bordes de Piscinas y Carriles:** Azul UNFV (`#1B365D`) o Gris oscuro.
* **Fondo de Tareas AS-IS con dolor:** Relleno rojo suave (`#FEE2E2`), borde rojo (`#EF4444`).
* **Fondo de Tareas TO-BE automatizadas (Carril 4):** Relleno verde suave (`#DCFCE7`), borde verde (`#16A34A`).
* **Fondo de Tareas de Usuario normales:** Blanco o celeste muy suave (`#F0F9FF`), borde azul pizarra (`#0284C7`).

---

## 📤 INSTRUCCIONES DE EXPORTACIÓN Y ENTREGA
1. Una vez terminado cada diagrama en Bizagi:
   * Ir al menú superior $\rightarrow$ **Exportar / Publicar** $\rightarrow$ **Imagen**.
   * Formato: **PNG**.
   * Calidad: Configurar a **300 DPI** o resolución máxima de página (evita capturas con `Win + Shift + S` para no perder nitidez).
2. Guardar las imágenes con estos nombres:
   * `AS_IS_BPMN_PROYECTO_GADI.png`
   * `TO_BE_BPMN_PROYECTO_GADI.png`
3. Guardar el archivo nativo del modelador como:
   * `MODELADO_PROCESOS_GADI_BIZAGI.bpm`
4. Compartir los archivos con el equipo para insertarlos en el Word en formato **APA 7** con sus respectivas leyendas.
