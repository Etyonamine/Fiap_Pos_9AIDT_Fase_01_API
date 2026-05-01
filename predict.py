import numpy as np
import pandas as pd

BINARY_COLS = [
    'VIOL_FISIC', 'VIOL_PSICO', 'VIOL_TORT', 'VIOL_FINAN',
    'VIOL_NEGLI', 'VIOL_INFAN', 'VIOL_LEGAL', 'VIOL_OUTR',
    'LES_AUTOP', 'AUTOR_ALCO', 'OUT_VEZES'
]

CAT_COLS = ['CS_GESTANT', 'CS_RACA', 'CS_ESCOL_N', 'LOCAL_OCOR', 'AUTOR_SEXO']


def preprocess_input(data: dict, feature_columns: list, imputer) -> np.ndarray:
    row = {}

    # 1. Numérica
    row['IDADE_ANOS'] = data.get('IDADE_ANOS', np.nan)

    # 2. Binárias: 1→1, 2→0, 9/ausente→NaN
    for col in BINARY_COLS:
        v = data.get(col, 9)
        row[col] = 1.0 if v == 1 else (0.0 if v == 2 else np.nan)

    # 3. One-Hot para categóricas (replica o pd.get_dummies do treino)
    for col in CAT_COLS:
        v = data.get(col, None)
        col_dummies = [c for c in feature_columns if c.startswith(col + '_')]
        for dummy in col_dummies:
            cat_val = float(dummy.split('_')[-1])  # ex: CS_GESTANT_5.0 → 5.0
            row[dummy] = 1.0 if (v is not None and float(v) == cat_val) else 0.0

    # 4. Monta DataFrame na ordem exata do treino
    df = pd.DataFrame([row], columns=feature_columns)

    # 5. Imputa valores ausentes
    X = imputer.transform(df)
    return X


def predict(data: dict, xgb_model, imputer, feature_columns) -> dict:
    X = preprocess_input(data, feature_columns, imputer)
    prob = xgb_model.predict_proba(X)[0][1]  # probabilidade de violência sexual
    label = int(prob >= 0.5)  # 1=violência sexual, 0=sem violência sexual
    return {
        "probabilidade_viol_sexual": round(float(prob), 4),
        "classificacao": "violencia_sexual" if label else "sem_violencia_sexual",
        "alerta": bool(prob >= 0.5),
    }
