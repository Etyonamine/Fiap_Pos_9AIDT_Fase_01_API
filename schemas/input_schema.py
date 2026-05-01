input_schema = {
    "type": "object",
    "properties": {
        "IDADE_ANOS": {
            "type": "integer",
            "minimum": 0,
            "maximum": 125,
            "description": "Idade em anos (0–125)"
        },
        "VIOL_FISIC": {
            "type": "integer",
            "enum": [1, 2, 9],
            "description": "Violência física: 1=Sim, 2=Não, 9=Ignorado"
        },
        "VIOL_PSICO": {
            "type": "integer",
            "enum": [1, 2, 9],
            "description": "Violência psicológica: 1=Sim, 2=Não, 9=Ignorado"
        },
        "LES_AUTOP": {
            "type": "integer",
            "enum": [1, 2, 9],
            "description": "Lesão autoprovocada: 1=Sim, 2=Não, 9=Ignorado"
        },
        "AUTOR_ALCO": {
            "type": "integer",
            "enum": [1, 2, 9],
            "description": "Autor sob efeito de álcool: 1=Sim, 2=Não, 9=Ignorado"
        },
        "OUT_VEZES": {
            "type": "integer",
            "enum": [1, 2, 9],
            "description": "Ocorrência em outras vezes: 1=Sim, 2=Não, 9=Ignorado"
        },
        "CS_GESTANT": {
            "type": "integer",
            "enum": [1, 2, 3, 4, 5, 6, 8],
            "description": (
                "Gestante: 1=1º tri, 2=2º tri, 3=3º tri, "
                "4=Idade gestacional ignorada, 5=Não gestante, "
                "6=Não se aplica, 8=Não informado"
            )
        },
        "CS_RACA": {
            "type": "integer",
            "enum": [1, 2, 3, 4, 5],
            "description": "Raça/cor: 1=Branca, 2=Preta, 3=Amarela, 4=Parda, 5=Indígena"
        },
        "CS_ESCOL_N": {
            "type": "integer",
            "enum": [0,1,2,3,4,5,6,7,8,10],
            "description": (
                "Escolaridade: 0=Sem escolaridade, 1=Fund. I incomp., "
                "2=Fund. I comp., 3=Fund. II incomp., 4=Fund. II comp., "
                "5=Médio incomp., 6=Médio comp., 7=Superior incomp., "
                "8=Superior comp., 10=Não informado"
            )
        },
        "LOCAL_OCOR": {
            "type": "integer",
            "enum": [1,2,3,4,5,6,7,8],
            "description": (
                "Local da ocorrência: 1=Residência, 2=Hab. coletiva, "
                "3=Escola, 4=Esporte, 5=Bar/Boate, 6=Via pública, "
                "7=Comércio, 8=Indústria"
            )
        },
        "AUTOR_SEXO": {
            "type": "integer",
            "enum": [1,2,3,4],
            "description": "Sexo do autor: 1=Masculino, 2=Feminino, 3=Ambos, 4=Ignorado"
        },
        "indice_probabilidade": {
            "type": "number",
            "format": "float",
            "minimum": 0.3,
            "maximum": 1,
            "description": "Índice decimal de probabilidade (0–1) fornecido como entrada"
        }
    },
    "required": ["IDADE_ANOS", "CS_RACA", "CS_ESCOL_N"]
}
