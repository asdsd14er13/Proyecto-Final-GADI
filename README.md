# Proyecto Final GADI (2026)
## Sistema Inteligente de Evaluación Adaptativa y Personalización del Aprendizaje Universitario
**Institución:** Universidad Nacional Federico Villarreal (UNFV) – FIEI  
**Docente:** Mg. Ing. Ivan Crispin Sanchez  
**Curso:** Gestión y Análisis de Datos e Información (GADI)  

---

## 📁 Estructura del Proyecto

```text
Proyecto Final GADI/
├── .agents/
│   └── skills/                     <- Skills instaladas y activas para Antigravity
│       ├── academic-paper/         <- Redacción formal del informe académico (APA 7)
│       ├── academic-paper-reviewer/<- Auditoría contra rúbrica de 20 puntos
│       ├── algorithm-design/       <- Pseudocódigo y diagramas Mermaid/UML
│       ├── backward-traceability/  <- Trazabilidad código/SQL <-> métricas del informe
│       ├── citation-management/    <- Manejo y verificación de citas/BibTeX
│       ├── data-analysis/          <- Análisis exploratorio y reglas de calidad
│       ├── deep-research/          <- Investigación profunda de literatura
│       ├── experiment-code/        <- Modelado y experimentos en Python (LR vs RF)
│       ├── literature-search/      <- Búsqueda de literatura científica
│       └── self-review/            <- Autoevaluación y coherencia interna
├── DATASET/                        <- Datasets oficiales filtrados y limpios
│   ├── UCI/                        <- data.csv (4,424 filas x 37 columnas)
│   ├── TUNI/                       <- Matricula 2025-II e institucional
│   └── ENAHO_2023/                 <- INEI ENAHO Módulos 300 y 500 con diccionarios
├── DOCUMENTACION/                  <- Toda la documentación, pautas y referencias
│   ├── oficial/                    <- Proyecto_Final_GADI_IA_2026.docx, ficha tecnica, requerimientos
│   ├── guias_internas/             <- Plan Maestro (05), Decisiones técnicas, Hoja de ruta
│   ├── clases/                     <- Diapositivas y material de clase del docente
│   └── bibliografia_papers/        <- Tablas consolidadas y PDFs descargados
│       └── papers_validados/       <- 12 papers en español + 4 en inglés validados
├── DATABASE_SQL/                   <- Scripts SQL Server (DataMart, staging, hechos)
├── ETL_SSIS/                       <- Proyecto Visual Studio de Integration Services (por desarrollar)
├── SSAS_OLAP/                      <- Proyecto Analysis Services para cubos multidimensionales (por desarrollar)
├── ML_PYTHON/                      <- Notebooks, scripts de IA y outputs de modelos
│   └── outputs/                    <- Resultados de comparación y predicciones
├── POWER_BI/                       <- Archivo .pbix para Dashboards y What-If (por desarrollar)
└── tools/                          <- Herramientas y servidores auxiliares
    └── academic-search-mcp/        <- Servidor MCP para búsquedas académicas en vivo
```

---

## 🎯 Próximo Paso Inmediato (Fase A0 y A1 del Plan Maestro)
1. **Fase A0 (Alineación y Alcance):** Redacción de la ficha de alcance de 1 página (cerrando D1 a D4).
2. **Fase A1 (Investigación):** Consolidación de la matriz bibliográfica con los 16 papers ya validados + normativas UNFV.
3. **Fase A2 y A3:** Redacción de la Introducción, Capítulo I (con diagramas AS-IS y TO-BE) y Capítulo II (Marco Teórico con bloques de aplicación técnica).
