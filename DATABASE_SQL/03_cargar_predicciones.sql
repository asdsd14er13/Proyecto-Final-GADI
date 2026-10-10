/* Importa outputs/predicciones_prueba.csv a stg.PrediccionesUCI desde SSMS.
   Son predicciones del conjunto de prueba para evaluación, no estudiantes reales identificables.
*/
SET XACT_ABORT ON;
BEGIN TRANSACTION;
TRUNCATE TABLE dw.FactPrediccion;
INSERT INTO dw.FactPrediccion(source_row_id,stage_key,predicted_outcome_key,
 actual_outcome_key,source_key,model_name,prob_dropout,prob_enrolled,prob_graduate)
SELECT p.source_row_id,e.stage_key,pred.outcome_key,actual.outcome_key,
 f.source_key,p.model_name,p.prob_dropout,p.prob_enrolled,p.prob_graduate
FROM stg.PrediccionesUCI p
JOIN dw.DimEtapa e ON e.stage_code=p.stage
JOIN dw.DimResultado pred ON pred.outcome_code=p.prediction
JOIN dw.DimResultado actual ON actual.outcome_code=p.actual_for_evaluation
JOIN dw.DimFuente f ON f.source_code='UCI697';
COMMIT TRANSACTION;
GO
SELECT COUNT_BIG(*) AS predicciones_cargadas,
       AVG(prob_dropout) AS probabilidad_media_abandono
FROM dw.FactPrediccion;
