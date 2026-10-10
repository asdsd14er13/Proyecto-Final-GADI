/* Hecho peruano de matrícula agregada, separado del DataMart UCI.
   No almacena GUID ni atributos personales. Carga solo el CSV agregado de Python.
*/
IF SCHEMA_ID('stg') IS NULL EXEC('CREATE SCHEMA stg');
IF SCHEMA_ID('dw') IS NULL EXEC('CREATE SCHEMA dw');
GO
DROP TABLE IF EXISTS dw.FactMatriculaTUNI;
DROP TABLE IF EXISTS stg.MatriculaTUNI;
DROP TABLE IF EXISTS dw.DimLocalTUNI;
DROP TABLE IF EXISTS dw.DimProgramaTUNI;
DROP TABLE IF EXISTS dw.DimPeriodoTUNI;
DROP TABLE IF EXISTS dw.DimInstitucionTUNI;
GO
CREATE TABLE stg.MatriculaTUNI (
 institution_code NVARCHAR(30) NOT NULL, institution_name NVARCHAR(250) NULL,
 management_type NVARCHAR(100) NULL, period_code NVARCHAR(30) NOT NULL,
 academic_level NVARCHAR(120) NULL, siu_program_code NVARCHAR(40) NOT NULL,
 group3_code NVARCHAR(40) NULL, group3_name NVARCHAR(200) NULL,
 program_name NVARCHAR(250) NULL, main_campus NVARCHAR(20) NULL,
 local_code NVARCHAR(40) NOT NULL, department NVARCHAR(120) NULL,
 province NVARCHAR(120) NULL, district NVARCHAR(120) NULL,
 catalog_institution_name NVARCHAR(250) NULL, institution_type NVARCHAR(120) NULL,
 catalog_match BIT NOT NULL,
 matricula_count BIGINT NOT NULL CHECK (matricula_count >= 5));
CREATE TABLE dw.DimInstitucionTUNI (
 institution_key INT IDENTITY PRIMARY KEY, institution_code NVARCHAR(30) NOT NULL UNIQUE,
 institution_name NVARCHAR(250) NULL, management_type NVARCHAR(100) NULL,
 catalog_institution_name NVARCHAR(250) NULL, institution_type NVARCHAR(120) NULL,
 catalog_match BIT NOT NULL);
CREATE TABLE dw.DimProgramaTUNI (
 program_key INT IDENTITY PRIMARY KEY, institution_code NVARCHAR(30) NOT NULL,
 siu_program_code NVARCHAR(40) NOT NULL, program_name NVARCHAR(250) NULL,
 academic_level NVARCHAR(120) NULL, group3_code NVARCHAR(40) NULL,
 group3_name NVARCHAR(200) NULL,
 CONSTRAINT UQ_DimProgramaTUNI UNIQUE(institution_code,siu_program_code));
CREATE TABLE dw.DimLocalTUNI (
 local_key INT IDENTITY PRIMARY KEY, institution_code NVARCHAR(30) NOT NULL,
 local_code NVARCHAR(40) NOT NULL, department NVARCHAR(120) NULL,
 province NVARCHAR(120) NULL, district NVARCHAR(120) NULL,
 main_campus NVARCHAR(20) NULL,
 CONSTRAINT UQ_DimLocalTUNI UNIQUE(institution_code,local_code));
CREATE TABLE dw.DimPeriodoTUNI (
 period_key INT IDENTITY PRIMARY KEY, period_code NVARCHAR(30) NOT NULL UNIQUE,
 period_name NVARCHAR(60) NOT NULL);
CREATE TABLE dw.FactMatriculaTUNI (
 institution_key INT NOT NULL, program_key INT NOT NULL,
 local_key INT NOT NULL, period_key INT NOT NULL,
 matricula_count BIGINT NOT NULL,
 CONSTRAINT PK_FactMatriculaTUNI PRIMARY KEY(institution_key,program_key,local_key,period_key),
 CONSTRAINT FK_Mat_Inst FOREIGN KEY(institution_key) REFERENCES dw.DimInstitucionTUNI(institution_key),
 CONSTRAINT FK_Mat_Prog FOREIGN KEY(program_key) REFERENCES dw.DimProgramaTUNI(program_key),
 CONSTRAINT FK_Mat_Local FOREIGN KEY(local_key) REFERENCES dw.DimLocalTUNI(local_key),
 CONSTRAINT FK_Mat_Period FOREIGN KEY(period_key) REFERENCES dw.DimPeriodoTUNI(period_key));
GO
