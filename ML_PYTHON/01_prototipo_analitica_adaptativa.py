# %% [markdown]
# Prototipo práctico: progreso y alerta académica
#
# Este notebook prepara el dataset público UCI y compara modelos en dos momentos:
# ingreso y cierre del primer semestre. Es una prueba retrospectiva con datos de
# Portugal; no valida predicciones para estudiantes peruanos.
#
# Privacidad: la IA no usa filas de matrícula TUNI ni atributos personales. Una
# sección separada produce conteos TUNI por institución/programa/local/periodo.

# %%
from pathlib import Path
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (classification_report, confusion_matrix,
    ConfusionMatrixDisplay, balanced_accuracy_score, f1_score, recall_score)

ROOT = Path.cwd()
if not (ROOT / 'data.csv').exists() and (ROOT.parent / 'data.csv').exists():
    ROOT = ROOT.parent
DATA = ROOT / 'data.csv'
OUT = ROOT / 'outputs'
OUT.mkdir(exist_ok=True)
print('Carpeta del proyecto:', ROOT)

# %% [markdown]
## 1. Revisar fuente y objetivo

# Solo inspeccionamos nombres de columnas y conteos de UCI. En esta primera sección
# no abrimos filas de matrícula TUNI; el objetivo UCI es abandono, permanencia o
# egreso, no una nota de aprobado/desaprobado.

# %%
uci = pd.read_csv(DATA, sep=';', encoding='utf-8-sig')
uci.columns = [c.strip() for c in uci.columns]
print(f'UCI: {uci.shape[0]:,} filas, {uci.shape[1]} columnas')
print('Clases del resultado:', sorted(uci['Target'].dropna().unique().tolist()))
print('Columnas:', list(uci.columns))
print('Catálogo institucional disponible:', (ROOT / 'institucional.csv').exists())
print('Matrícula TUNI disponible (se agrega en su sección propia):', (ROOT / 'matriculado_2025_II.csv').exists())

# %%
display(uci['Target'].value_counts(dropna=False).rename('cantidad').to_frame())
print('Duplicados exactos:', int(uci.duplicated().sum()))
print('Celdas vacías:', int(uci.isna().sum().sum()))
ax = uci['Target'].value_counts().plot(kind='bar', color='#4267a9', rot=0)
ax.set_title('Distribución del resultado académico en UCI')
ax.set_xlabel('Resultado'); ax.set_ylabel('Estudiantes')
plt.tight_layout(); plt.show()

# %% [markdown]
## 2. Definir el momento de la predicción

# Ingreso usa antecedentes disponibles al matricularse. La actualización agrega
# solo datos del primer semestre. Excluimos variables del segundo semestre para
# evitar fuga de información. La nota UCI de primer semestre ya está en escala
# 0–20; no se reescala ni se impone el corte peruano de 11 al resultado UCI.
# Los códigos de programa son portugueses y no se renombran con carreras TUNI.

# %%
TARGET = 'Target'
base_features = [
    'Application mode', 'Application order', 'Course',
    'Daytime/evening attendance', 'Previous qualification',
    'Previous qualification (grade)', 'Admission grade'
]
first_sem_features = [
    'Curricular units 1st sem (credited)', 'Curricular units 1st sem (enrolled)',
    'Curricular units 1st sem (evaluations)', 'Curricular units 1st sem (approved)',
    'Curricular units 1st sem (grade)', 'Curricular units 1st sem (without evaluations)'
]
required = base_features + first_sem_features + [TARGET]
missing = sorted(set(required) - set(uci.columns))
if missing:
    raise ValueError(f'Faltan columnas esperadas: {missing}')
print('Rango observado de nota primer semestre:',
      uci['Curricular units 1st sem (grade)'].min(), 'a',
      uci['Curricular units 1st sem (grade)'].max())

# %% [markdown]
## 3. Separar entrenamiento y prueba

# El identificador de fila es técnico y artificial. Se usa para separar ambos
# momentos del mismo registro en un solo conjunto (entrenamiento o prueba), nunca
# como predictor ni como identidad real.

# %%
df = uci[required].copy()
df['_row_id'] = np.arange(len(df), dtype=int)
train_ids, test_ids = train_test_split(
    df['_row_id'], test_size=0.25, random_state=42, stratify=df[TARGET])
train = df[df['_row_id'].isin(train_ids)]
test = df[df['_row_id'].isin(test_ids)]
print(f'Entrenamiento: {len(train):,}; prueba: {len(test):,}')
display((test[TARGET].value_counts(normalize=True)*100).round(1)
        .rename('porcentaje').to_frame())

# %% [markdown]
## 4. Entrenar y comparar

# Se compara regresión logística con Random Forest. F1 macro pondera por igual las
# tres categorías; recall de abandono mide cuántos casos de abandono se recuperan.
# El pipeline ajusta imputación, escalado y codificación solo con entrenamiento.

# %%
def build_pipeline(X, model):
    numeric = X.select_dtypes(include=['number']).columns.tolist()
    categorical = [c for c in X.columns if c not in numeric]
    prep = ColumnTransformer([
        ('num', Pipeline([('imputer', SimpleImputer(strategy='median')),
                         ('scale', StandardScaler())]), numeric),
        ('cat', Pipeline([('imputer', SimpleImputer(strategy='most_frequent')),
                         ('onehot', OneHotEncoder(handle_unknown='ignore'))]), categorical)
    ])
    return Pipeline([('prep', prep), ('model', model)])

results, fitted = [], {}
for stage, features in [('ingreso', base_features),
                        ('fin_primer_semestre', base_features + first_sem_features)]:
    X_train, X_test = train[features], test[features]
    y_train, y_test = train[TARGET], test[TARGET]
    models = {
        'Regresión logística': LogisticRegression(max_iter=2000, class_weight='balanced'),
        'Random Forest': RandomForestClassifier(n_estimators=300, min_samples_leaf=3,
            class_weight='balanced_subsample', random_state=42, n_jobs=-1)
    }
    for model_name, estimator in models.items():
        pipe = build_pipeline(X_train, estimator)
        pipe.fit(X_train, y_train)
        pred = pipe.predict(X_test)
        drop_recall = recall_score(y_test, pred, labels=['Dropout'],
                                  average=None, zero_division=0)[0]
        results.append({'momento': stage, 'modelo': model_name,
            'balanced_accuracy': balanced_accuracy_score(y_test, pred),
            'f1_macro': f1_score(y_test, pred, average='macro'),
            'recall_abandono': drop_recall})
        fitted[(stage, model_name)] = (pipe, pred, features)
scores = pd.DataFrame(results).sort_values(['momento','f1_macro'],
                                           ascending=[True,False])
display(scores.round(3))

# %% [markdown]
## 5. Evaluar errores y exportar predicciones de prueba

# Seleccionamos provisionalmente por F1 macro en la etapa final. La probabilidad
# es una señal para revisión humana, no una etiqueta de “mal estudiante” ni una
# decisión académica automática.

# %%
best_row = scores[scores['momento']=='fin_primer_semestre'].sort_values(
    'f1_macro', ascending=False).iloc[0]
best_key = ('fin_primer_semestre', best_row['modelo'])
best_pipe, best_pred, best_features = fitted[best_key]
print('Modelo provisional:', best_row['modelo'])
print(classification_report(test[TARGET], best_pred, zero_division=0))
labels = list(best_pipe.named_steps['model'].classes_)
ConfusionMatrixDisplay(confusion_matrix(test[TARGET], best_pred, labels=labels),
                       display_labels=labels).plot(cmap='Blues', xticks_rotation=30)
plt.title('Matriz de confusión: cierre del primer semestre')
plt.tight_layout(); plt.show()

proba = best_pipe.predict_proba(test[best_features])
predictions = pd.DataFrame({
    'source_row_id': test['_row_id'].to_numpy(),
    'stage': 'fin_primer_semestre',
    'prediction': best_pipe.predict(test[best_features]),
    'actual_for_evaluation': test[TARGET].to_numpy()})
for j, class_name in enumerate(best_pipe.named_steps['model'].classes_):
    predictions[f'prob_{str(class_name).lower()}'] = proba[:, j]
predictions['model_name'] = best_row['modelo']
predictions.to_csv(OUT / 'predicciones_prueba.csv', index=False)
scores.to_csv(OUT / 'comparacion_modelos.csv', index=False)
display(predictions.head(10).round(3))

# %% [markdown]
## 6. Generar staging para SQL Server

# Grano: una fila UCI por momento de evaluación. No inventamos fecha, universidad
# ni carrera peruana. El script SQL crea dimensiones de etapa, resultado y fuente,
# y la tabla de hechos de progreso. El catálogo institucional TUNI queda separado.

# %%
warehouse_rows = []
for _, row in df.iterrows():
    for stage, cols in [('ingreso', []), ('fin_primer_semestre', first_sem_features)]:
        rec = {'source_row_id': int(row['_row_id']), 'stage': stage,
               'actual_outcome': row[TARGET]}
        for col in first_sem_features:
            rec[col] = row[col] if col in cols else np.nan
        warehouse_rows.append(rec)
fact = pd.DataFrame(warehouse_rows).rename(columns={
    'Curricular units 1st sem (credited)': 'curricular_credited',
    'Curricular units 1st sem (enrolled)': 'curricular_enrolled',
    'Curricular units 1st sem (evaluations)': 'curricular_evaluations',
    'Curricular units 1st sem (approved)': 'curricular_approved',
    'Curricular units 1st sem (grade)': 'curricular_grade',
    'Curricular units 1st sem (without evaluations)': 'curricular_without_evaluations'})
fact.to_csv(OUT / 'stg_progreso_uci.csv', index=False)
print('Staging generado:', len(fact), 'filas. Salida:', OUT)
display(fact.groupby('stage').size().rename('filas').to_frame())

# %% [markdown]
## 7. Alcance y siguiente información necesaria

# El modelo es retrospectivo y corresponde a una institución portuguesa. No
# permite concluir que estudiantes peruanos estén en riesgo. Para validarlo en
# Perú hace falta una muestra académica local seudonimizada y autorizada, con
# resultados por ciclo y fechas que indiquen cuándo se conocía cada dato. El
# catálogo institucional y la matrícula TUNI se procesan en una sección aparte:
# generan conteos peruanos y no se conectan con las filas UCI.

# %% [markdown]
## 8. Contexto peruano agregado con los archivos TUNI

# Esta parte es independiente de la IA UCI. Lee únicamente campos de institución,
# programa, local y periodo del archivo de matrícula; **no lee GUID, edad, sexo,
# nacionalidad, nacimiento ni discapacidad**. Agrupa y suprime grupos con menos de
# 5 matrículas para reducir el riesgo de revelar personas. El catálogo institucional
# se usa para enriquecer la dimensión de institución por código INEI. Los nombres
# de programa salen de la propia fuente de matrícula: no se fuerza una equivalencia
# entre distintos códigos de programa.

# %%
TUNI_MAT = ROOT / 'matriculado_2025_II.csv'
TUNI_CAT = ROOT / 'institucional.csv'
TUNI_OUT = OUT / 'stg_matricula_tuni.csv'
CAT_OUT = OUT / 'stg_catalogo_tuni.csv'
safe_cols = [
    'CODIGO_INEI', 'NOMBRE_ENTIDAD', 'TIPO_GESTION', 'PERIODO_ESTANDARIZADO',
    'NIVEL_ACADEMICO', 'CODIGO_SIU_PROGRAMA', 'CODIGO_GRUPO_3',
    'NOMBRE_GRUPO_3', 'NOMBRE_PROGRAMA', 'ES_LOCAL_PRINCIPAL',
    'CODIGO_LOCAL', 'DEPARTAMENTO_LOCAL', 'PROVINCIA_LOCAL', 'DISTRITO_LOCAL']

# El CSV de catálogo tiene filas con formatos inconsistentes en algunas columnas
# posteriores. Usamos solo sus tres primeros campos y aceptamos solo códigos INEI
# con nueve dígitos. No interpretamos las columnas geográficas/programáticas restantes.
cat_rows = []
with TUNI_CAT.open('r', encoding='latin1', newline='') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        if len(row) >= 3 and row[0].strip().isdigit() and len(row[0].strip()) == 9 and row[1].strip():
            cat_rows.append({
                'institution_code': row[0].strip(),
                'catalog_institution_name': row[1].strip(),
                'institution_type': row[2].strip()})
catalog = pd.DataFrame(cat_rows).drop_duplicates()
catalog = catalog.drop_duplicates(['institution_code'])
catalog.to_csv(CAT_OUT, index=False)

# Procesa el CSV de matrícula por bloques. No se seleccionan columnas personales.
partial = []
for chunk in pd.read_csv(TUNI_MAT, sep='|', usecols=safe_cols, dtype=str,
                         encoding='latin1', na_values=['<NULL>'], chunksize=150_000):
    chunk = chunk.fillna('Sin dato')
    partial.append(chunk.groupby(safe_cols, dropna=False).size().rename('matricula_count'))
aggregated = (pd.concat(partial).groupby(level=list(range(len(safe_cols))))
              .sum().reset_index())
aggregated = aggregated.rename(columns={
    'CODIGO_INEI':'institution_code', 'NOMBRE_ENTIDAD':'institution_name',
    'TIPO_GESTION':'management_type', 'PERIODO_ESTANDARIZADO':'period_code',
    'NIVEL_ACADEMICO':'academic_level', 'CODIGO_SIU_PROGRAMA':'siu_program_code',
    'CODIGO_GRUPO_3':'group3_code', 'NOMBRE_GRUPO_3':'group3_name',
    'NOMBRE_PROGRAMA':'program_name', 'ES_LOCAL_PRINCIPAL':'main_campus',
    'CODIGO_LOCAL':'local_code', 'DEPARTAMENTO_LOCAL':'department',
    'PROVINCIA_LOCAL':'province', 'DISTRITO_LOCAL':'district'})
enriched = aggregated.merge(catalog, on='institution_code', how='left')
enriched['catalog_match'] = enriched['catalog_institution_name'].notna().astype('int8')
suppressed = int((enriched['matricula_count'] < 5).sum())
safe_aggregate = enriched[enriched['matricula_count'] >= 5].copy()
output_cols = [
    'institution_code','institution_name','management_type','period_code',
    'academic_level','siu_program_code','group3_code','group3_name','program_name',
    'main_campus','local_code','department','province','district',
    'catalog_institution_name','institution_type','catalog_match','matricula_count']
safe_aggregate = safe_aggregate[output_cols]
safe_aggregate.to_csv(TUNI_OUT, index=False)
print('Grupos agregados antes de supresión:', len(enriched))
print('Grupos pequeños suprimidos (menos de 5 matrículas):', suppressed)
print('Grupos seguros exportados:', len(safe_aggregate))
print('Cobertura de enriquecimiento con catálogo:',
      round(safe_aggregate['catalog_match'].mean()*100, 1), '%')
print('CSV agregado creado:', TUNI_OUT)
print('Instituciones únicas válidas en catálogo:', len(catalog))

# %% [markdown]
## 9. Qué representa el análisis peruano

# El archivo agregado permite describir matrícula por institución, programa,
# local y periodo, y aporta contexto nacional al proyecto. No tiene las mismas
# unidades, cohortes ni etiquetas que UCI; por eso no alimenta el clasificador.
# El catálogo añade el nombre y tipo de institución cuando coincide el código
# INEI. Los nombres de programas provienen de la propia matrícula. No se usan los
# códigos de programa del catálogo para declarar que una carrera sea equivalente
# a otra ni para cruzar TUNI con UCI.
