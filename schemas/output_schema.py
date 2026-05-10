output_schema = {
    "type": "object",
    "properties": {
        "probabilidade_viol_sexual": {
            "type": "number",
            "minimum": 0,
            "maximum": 1,
            "description": "Probabilidade estimada (0–1)"
        },
        "classificacao": {
            "type": "string",
            "enum": ["violencia_sexual", "sem_violencia_sexual"],
            "description": "Classificação final do caso"
        },
        "alerta": {
            "type": "boolean",
            "description": "True se probabilidade ≥ indice_probabilidade (padrão 0.5)"
        }
    }
}
