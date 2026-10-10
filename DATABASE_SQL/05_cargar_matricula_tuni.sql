/* Importa outputs/stg_matricula_tuni.csv en stg.MatriculaTUNI antes de ejecutar. */
SET XACT_ABORT ON;
BEGIN TRANSACTION;

INSERT INTO dw.DimInstitucionTUNI(institution_code,institution_name,management_type,
 catalog_institution_name,institution_type,catalog_match)
SELECT DISTINCT s.institution_code,s.institution_name,s.management_type,
 s.catalog_institution_name,s.institution_type,s.catalog_match
FROM stg.MatriculaTUNI s
WHERE NOT EXISTS (SELECT 1 FROM dw.DimInstitucionTUNI d
                  WHERE d.institution_code=s.institution_code);

INSERT INTO dw.DimProgramaTUNI(institution_code,siu_program_code,program_name,
 academic_level,group3_code,group3_name)
SELECT DISTINCT s.institution_code,s.siu_program_code,s.program_name,s.academic_level,
 s.group3_code,s.group3_name
FROM stg.MatriculaTUNI s
WHERE NOT EXISTS (SELECT 1 FROM dw.DimProgramaTUNI d
 WHERE d.institution_code=s.institution_code AND d.siu_program_code=s.siu_program_code);

INSERT INTO dw.DimLocalTUNI(institution_code,local_code,department,province,district,main_campus)
SELECT DISTINCT s.institution_code,s.local_code,s.department,s.province,s.district,s.main_campus
FROM stg.MatriculaTUNI s
WHERE NOT EXISTS (SELECT 1 FROM dw.DimLocalTUNI d
 WHERE d.institution_code=s.institution_code AND d.local_code=s.local_code);

INSERT INTO dw.DimPeriodoTUNI(period_code,period_name)
SELECT DISTINCT s.period_code,s.period_code FROM stg.MatriculaTUNI s
WHERE NOT EXISTS (SELECT 1 FROM dw.DimPeriodoTUNI d WHERE d.period_code=s.period_code);

TRUNCATE TABLE dw.FactMatriculaTUNI;
INSERT INTO dw.FactMatriculaTUNI(institution_key,program_key,local_key,period_key,matricula_count)
SELECT i.institution_key,p.program_key,l.local_key,t.period_key,SUM(s.matricula_count)
FROM stg.MatriculaTUNI s
JOIN dw.DimInstitucionTUNI i ON i.institution_code=s.institution_code
JOIN dw.DimProgramaTUNI p ON p.institution_code=s.institution_code AND p.siu_program_code=s.siu_program_code
JOIN dw.DimLocalTUNI l ON l.institution_code=s.institution_code AND l.local_code=s.local_code
JOIN dw.DimPeriodoTUNI t ON t.period_code=s.period_code
GROUP BY i.institution_key,p.program_key,l.local_key,t.period_key;

COMMIT TRANSACTION;
GO
SELECT t.period_name,i.institution_name,SUM(f.matricula_count) AS matrículas_agregadas
FROM dw.FactMatriculaTUNI f
JOIN dw.DimPeriodoTUNI t ON t.period_key=f.period_key
JOIN dw.DimInstitucionTUNI i ON i.institution_key=f.institution_key
GROUP BY t.period_name,i.institution_name
ORDER BY t.period_name,i.institution_name;
