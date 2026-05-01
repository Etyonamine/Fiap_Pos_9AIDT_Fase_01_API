import decimal
import numpy as np
import pandas as pd
import logging
from app import app
from flask import Flask, request, jsonify, redirect
from model_predict import predict as run_predict


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@app.route("/predict", methods=["POST"])
def predict():
    """
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/InputModel'
    responses:
      200:
        description: Resultado da predição
        schema:
          $ref: '#/definitions/OutputModel'
    """
    data = request.get_json()
    indice_probabilidade = data.get("indice_probabilidade")

    # Faz o log no console
    logger.info(f"Indice de probabilidade recebido: {indice_probabilidade}")

    result = run_predict(data, xgb_model, imputer, feature_columns, indice_probabilidade)
    return jsonify(result)

BINARY_COLS = [
    'VIOL_FISIC', 'VIOL_PSICO', 'VIOL_TORT', 'VIOL_FINAN',
    'VIOL_NEGLI', 'VIOL_INFAN', 'VIOL_LEGAL', 'VIOL_OUTR',
    'LES_AUTOP', 'AUTOR_ALCO', 'OUT_VEZES'
]

CAT_COLS = ['CS_GESTANT', 'CS_RACA', 'CS_ESCOL_N', 'LOCAL_OCOR', 'AUTOR_SEXO']


def preprocess_input(data: dict, feature_columns: list, imputer) -> np.ndarray:
    """Pré-processa o dicionário de entrada para o formato esperado pelo modelo.

    Etapas:
    1. Extrai a variável numérica IDADE_ANOS (NaN quando ausente).
    2. Converte colunas binárias: 1 → 1.0, 2 → 0.0, 9/ausente → NaN.
    3. Aplica one-hot encoding nas colunas categóricas replicando o
       ``pd.get_dummies`` utilizado no treino (nomes no formato
       ``<COL>_<valor_float>``, ex.: ``CS_GESTANT_5.0``).
    4. Monta um DataFrame com as colunas exatamente na ordem do treino.
    5. Imputa valores ausentes usando o ``imputer`` fornecido.

    Args:
        data: Dicionário com os campos brutos da notificação.
        feature_columns: Lista ordenada de colunas gerada durante o treino.
        imputer: Objeto scikit-learn compatível com ``.transform()``.

    Returns:
        Array NumPy com shape ``(1, n_features)`` pronto para inferência.
    """
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
            try:
                cat_val = float(dummy.split('_')[-1])  # ex: CS_GESTANT_5.0 → 5.0
            except ValueError:
                cat_val = None
            row[dummy] = 1.0 if (v is not None and cat_val is not None and float(v) == cat_val) else 0.0

    # 4. Monta DataFrame na ordem exata do treino
    df = pd.DataFrame([row], columns=feature_columns)

    # 5. Imputa valores ausentes
    X = imputer.transform(df)
    return X


def predict(data: dict, xgb_model, imputer, feature_columns, indice_probabilidade: decimal.Decimal) -> dict:
    """Executa o pipeline completo de predição de violência sexual.

    Pré-processa os dados brutos, aplica o modelo XGBoost e retorna a
    probabilidade estimada, a classificação e um indicador de alerta.

    O threshold de classificação é 0.5: probabilidades ≥ 0.5 são
    classificadas como ``"violencia_sexual"`` e alerta ``true``.

    Args:
        data: Dicionário com os campos brutos da notificação.
        xgb_model: Modelo XGBoost carregado com ``joblib.load``.
        imputer: Imputer scikit-learn carregado com ``joblib.load``.
        feature_columns: Lista de colunas carregada com ``joblib.load``.

    Returns:
        Dicionário com as chaves:
        - ``probabilidade_viol_sexual`` (float): Probabilidade 0–1.
        - ``classificacao`` (str): ``"violencia_sexual"`` ou ``"sem_violencia_sexual"``.
        - ``alerta`` (bool): ``True`` se probabilidade ≥ 0.5.
    """
    X = preprocess_input(data, feature_columns, imputer)
    prob = xgb_model.predict_proba(X)[0][1]  # probabilidade de violência sexual
    label = int(prob >= 0.5)  # 1=violência sexual, 0=sem violência sexual
    return {
        "probabilidade_viol_sexual": round(float(prob), 4),
        "classificacao": "violencia_sexual" if label else "sem_violencia_sexual",
        "alerta": bool(prob >= indice_probabilidade),
    }
