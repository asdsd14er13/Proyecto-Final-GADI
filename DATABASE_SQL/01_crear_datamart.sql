/* Prototipo académico UCI (Portugal), no datos peruanos.
   No importar aquí el CSV de matrícula TUNI: contiene datos personales.
*/
IF SCHEMA_ID('stg') IS NULL EXEC('CREATE SCHEMA stg');
IF SCHEMA_ID('dw') IS NULL EXEC('CREATE SCHEMA dw');
GO
DROP TABLE IF EXISTS dw.FactPrediccion;
DROP TABLE IF EXISTS dw.FactProgreso;
DROP TABLE IF EXISTS dw.DimResultado;
DROP TABLE IF EXISTS dw.DimEtapa;
DROP TABLE IF EXISTS dw.DimFuente;
DROP TABLE IF EXISTS stg.ProgresoUCI;
DROP TABLE IF EXISTS stg.PrediccionesUCI;
GO
CREATE TABLE stg.ProgresoUCI (
 source_row_id INT NOT NULL, stage NVARCHAR(40) NOT NULL,
 actual_outcome NVARCHAR(30) NOT NULL,
 curricular_credited FLOAT NULL, curricular_enrolled FLOAT NULL,
 curricular_evaluations FLOAT NULL, curricular_approved FLOAT NULL,
 curricular_grade FLOAT NULL, curricular_without_evaluations FLOAT NULL,
 CONSTRAINT PK_ProgresoUCI PRIMARY KEY (source_row_id, stage));
CREATE TABLE stg.PrediccionesUCI (
 source_row_id INT NOT NULL, stage NVARCHAR(40) NOT NULL,
 prediction NVARCHAR(30) NOT NULL, actual_for_evaluation NVARCHAR(30) NOT NULL,
 prob_dropout FLOAT NULL, prob_enrolled FLOAT NULL, prob_graduate FLOAT NULL,
 model_name NVARCHAR(100) NOT NULL,
 CONSTRAINT PK_PrediccionesUCI PRIMARY KEY (source_row_id, stage));
CREATE TABLE dw.DimEtapa (
 stage_key INT IDENTITY PRIMARY KEY, stage_code NVARCHAR(40) NOT NULL UNIQUE,
 stage_name NVARCHAR(100) NOT NULL);
CREATE TABLE dw.DimResultado (
 outcome_key INT IDENTITY PRIMARY KEY, outcome_code NVARCHAR(30) NOT NULL UNIQUE,
 outcome_name NVARCHAR(100) NOT NULL);
CREATE TABLE dw.DimFuente (
 source_key INT IDENTITY PRIMARY KEY, source_code NVARCHAR(30) NOT NULL UNIQUE,
 source_name NVARCHAR(150) NOT NULL, country_context NVARCHAR(100) NOT NULL);
CREATE TABLE dw.FactProgreso (
 source_row_id INT NOT NULL, stage_key INT NOT NULL, outcome_key INT NOT NULL,
 source_key INT NOT NULL, curricular_credited FLOAT NULL,
 curricular_enrolled FLOAT NULL, curricular_evaluations FLOAT NULL,
 curricular_approved FLOAT NULL, curricular_grade FLOAT NULL,
 curricular_without_evaluations FLOAT NULL,
 CONSTRAINT PK_FactProgreso PRIMARY KEY(source_row_id, stage_key),
 CONSTRAINT FK_Fact_Etapa FOREIGN KEY(stage_key) REFERENCES dw.DimEtapa(stage_key),
 CONSTRAINT FK_Fact_Resultado FOREIGN KEY(outcome_key) REFERENCES dw.DimResultado(outcome_key),
 CONSTRAINT FK_Fact_Fuente FOREIGN KEY(source_key) REFERENCES dw.DimFuente(source_key));
CREATE TABLE dw.FactPrediccion (
 source_row_id INT NOT NULL, stage_key INT NOT NULL,
 predicted_outcome_key INT NOT NULL, actual_outcome_key INT NOT NULL,
 source_key INT NOT NULL, model_name NVARCHAR(100) NOT NULL,
 prob_dropout FLOAT NULL, prob_enrolled FLOAT NULL, prob_graduate FLOAT NULL,
 CONSTRAINT PK_FactPrediccion PRIMARY KEY(source_row_id, stage_key),
 CONSTRAINT FK_Pred_Stage FOREIGN KEY(stage_key) REFERENCES dw.DimEtapa(stage_key),
 CONSTRAINT FK_PredictedOutcome FOREIGN KEY(predicted_outcome_key) REFERENCES dw.DimResultado(outcome_key),
 CONSTRAINT FK_ActualOutcome FOREIGN KEY(actual_outcome_key) REFERENCES dw.DimResultado(outcome_key),
 CONSTRAINT FK_Pred_Source FOREIGN KEY(source_key) REFERENCES dw.DimFuente(source_key));
GO
INSERT INTO dw.DimEtapa(stage_code,stage_name) VALUES
 ('ingreso',N'Al ingreso'),('fin_primer_semestre',N'Al cierre del primer semestre');
INSERT INTO dw.DimResultado(outcome_code,outcome_name) VALUES
 ('Dropout',N'Abandono (etiqueta fuente)'),('Enrolled',N'Continúa matriculado (etiqueta fuente)'),
 ('Graduate',N'Egreso (etiqueta fuente)');
INSERT INTO dw.DimFuente(source_code,source_name,country_context) VALUES
 ('UCI697',N'Predict Students Dropout and Academic Success',N'Portugal');
GO
