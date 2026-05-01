import logging

from flask import Flask, redirect, request, jsonify
from flasgger import Swagger
import joblib
from schemas.input_schema import input_schema
from schemas.output_schema import output_schema
from predict import predict


app = Flask(__name__)

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/",
}

swagger_template = {
    "info": {
        "title": "API de Predição de Violência Sexual",
        "description": "API que utiliza XGBoost para estimar probabilidade de violência sexual.",
        "version": "1.0.0",
    },
    "definitions": {
        "InputModel": input_schema,
        "OutputModel": output_schema
    }
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)



logger = logging.getLogger(__name__)

# declara antes para o linter saber que existem
xgb_model = None
imputer = None
feature_columns = None

_MODEL_FILES = {
    "xgb_model": "model/xgb_viol_sexu.joblib",
    "imputer": "model/imputer.joblib",
    "feature_columns": "model/feature_columns.joblib",
}

try:
    xgb_model = joblib.load(_MODEL_FILES["xgb_model"])
    imputer = joblib.load(_MODEL_FILES["imputer"])
    feature_columns = joblib.load(_MODEL_FILES["feature_columns"])
except FileNotFoundError as exc:
    raise SystemExit(
        f"Arquivo de modelo não encontrado: {exc}. "
        "Certifique-se de que os arquivos xgb_viol_sexu.joblib, "
        "imputer.joblib e feature_columns.joblib estão na pasta model/."
    ) from exc

@app.route("/", methods=["GET"])
def index():
    return redirect("/docs/") 

@app.route("/predict", methods=["POST"])
def predict():
    """
    Predição de violência sexual a partir de uma notificação.
    ---
    tags:
      - Predição
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - IDADE_ANOS
          properties:
            IDADE_ANOS:
              type: integer
              description: "Idade em anos (0–125)"
              example: 23
            VIOL_FISIC:
              type: integer
              description: "Violência física (1=Sim, 2=Não, 9=Ignorado)"
              example: 1
            VIOL_PSICO:
              type: integer
              description: "Violência psicológica (1=Sim, 2=Não, 9=Ignorado)"
              example: 1
            VIOL_TORT:
              type: integer
              description: "Tortura (1=Sim, 2=Não, 9=Ignorado)"
              example: 2
            VIOL_FINAN:
              type: integer
              description: "Violência financeira (1=Sim, 2=Não, 9=Ignorado)"
              example: 2
            VIOL_NEGLI:
              type: integer
              description: "Negligência (1=Sim, 2=Não, 9=Ignorado)"
              example: 2
            VIOL_INFAN:
              type: integer
              description: "Violência infantil (1=Sim, 2=Não, 9=Ignorado)"
              example: 2
            VIOL_LEGAL:
              type: integer
              description: "Violência legal (1=Sim, 2=Não, 9=Ignorado)"
              example: 2
            VIOL_OUTR:
              type: integer
              description: "Outros tipos de violência (1=Sim, 2=Não, 9=Ignorado)"
              example: 2
            LES_AUTOP:
              type: integer
              description: "Lesão autoprovocada (1=Sim, 2=Não, 9=Ignorado)"
              example: 2
            AUTOR_ALCO:
              type: integer
              description: "Autor sob efeito de álcool (1=Sim, 2=Não, 9=Ignorado)"
              example: 1
            OUT_VEZES:
              type: integer
              description: "Ocorreu outras vezes (1=Sim, 2=Não, 9=Ignorado)"
              example: 1
            CS_GESTANT:
              type: integer
              description: >
                Gestação (1=1º tri, 2=2º tri, 3=3º tri,
                4=Idade gestacional ignorada, 5=Não gestante,
                6=Não se aplica, 8=Não informado)
              example: 5
            CS_RACA:
              type: integer
              description: "Raça/cor (1=Branca, 2=Preta, 3=Amarela, 4=Parda, 5=Indígena)"
              example: 4
            CS_ESCOL_N:
              type: integer
              description: >
                Escolaridade (0=Sem escol., 1=Fund. I incomp., 2=Fund. I comp.,
                3=Fund. II incomp., 4=Fund. II comp., 5=Médio incomp.,
                6=Médio comp., 7=Superior incomp., 8=Superior comp.,
                10=Não informado)
              example: 3
            LOCAL_OCOR:
              type: integer
              description: >
                Local de ocorrência (1=Residência, 2=Hab. coletiva, 3=Escola,
                4=Esporte, 5=Bar/Boate, 6=Via pública, 7=Comércio, 8=Indústria)
              example: 1
            AUTOR_SEXO:
              type: integer
              description: "Sexo do autor (1=Masculino, 2=Feminino, 3=Ambos, 4=Ignorado)"
              example: 1
            indice_probabilidade:
              type: number
              format: float
              minimum: 0
              maximum: 1
              description: "Índice decimal de probabilidade (0–1) fornecido como entrada"
              exemplo: 0.4
    responses:
      200:
        description: Resultado da predição
        schema:
          type: object
          properties:
            probabilidade_viol_sexual:
              type: number
              format: float
              description: "Probabilidade estimada de violência sexual (0–1)"
              example: 0.8523
            classificacao:
              type: string
              description: '"violencia_sexual" ou "sem_violencia_sexual"'
              example: "violencia_sexual"
            alerta:
              type: boolean
              description: "true se probabilidade ≥ 0.5"
              example: true
      400:
        description: Requisição inválida (corpo ausente ou não é JSON)
        schema:
          type: object
          properties:
            error:
              type: string
              example: "O corpo da requisição deve ser um JSON válido."
      500:
        description: Erro interno do servidor
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Erro interno: <mensagem>"
    """
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "O corpo da requisição deve ser um JSON válido."}), 400

    try:
        indice_probabilidade = data["indice_probabilidade"]

        result = predict(data, xgb_model, imputer, feature_columns, indice_probabilidade)
    except Exception as exc:
        logger.exception("Erro ao processar predição: %s", exc)
        return jsonify({"error": "Erro interno ao processar a predição."}), 500

    return jsonify(result), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)