/* Primero importa outputs/stg_progreso_uci.csv a stg.ProgresoUCI con el asistente de SSMS. */
SET XACT_ABORT ON;
BEGIN TRANSACTION;
TRUNCATE TABLE dw.FactProgreso;
INSERT INTO dw.FactProgreso(source_row_id,stage_key,outcome_key,source_key,
 curricular_credited,curricular_enrolled,curricular_evaluations,curricular_approved,
 curricular_grade,curricular_without_evaluations)
SELECT s.source_row_id,e.stage_key,r.outcome_key,f.source_key,
 s.curricular_credited,s.curricular_enrolled,s.curricular_evaluations,
 s.curricular_approved,s.curricular_grade,s.curricular_without_evaluations
FROM stg.ProgresoUCI s
JOIN dw.DimEtapa e ON e.stage_code=s.stage
JOIN dw.DimResultado r ON r.outcome_code=s.actual_outcome
JOIN dw.DimFuente f ON f.source_code='UCI697';
COMMIT TRANSACTION;
GO
SELECT e.stage_name,r.outcome_name,COUNT_BIG(*) AS cantidad_registros
FROM dw.FactProgreso p JOIN dw.DimEtapa e ON e.stage_key=p.stage_key
JOIN dw.DimResultado r ON r.outcome_key=p.outcome_key
GROUP BY e.stage_name,r.outcome_name ORDER BY e.stage_name,r.outcome_name;
