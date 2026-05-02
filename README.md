# Fiap_Pos_9AIDT_Fase_01_API

API em Python (Flask + Flasgger) que embarca um modelo XGBoost para predição de violência sexual a partir dos campos brutos de uma notificação de violência.

## Estrutura do projeto

```
.
├── app.py               # Aplicação Flask com endpoint /predict e documentação Swagger
├── predict.py           # Pré-processamento e lógica de predição
├── requirements.txt     # Dependências Python
└── model/               # Arquivos do modelo (não versionados)
    ├── xgb_viol_sexu.joblib
    ├── imputer.joblib
    └── feature_columns.joblib
```

## Pré-requisitos

- Python 3.14+
- Arquivos de modelo em `model/` (gerados pelo pipeline de treino):
  - `xgb_viol_sexu.joblib`
  - `imputer.joblib`
  - `feature_columns.joblib`

## Instalação

```bash
pip install -r requirements.txt
```

## Execução

```bash
python app.py
```

A API estará disponível em `http://localhost:5000`.  
A documentação Swagger (Flasgger) estará em `http://localhost:5000/docs/`.

## Endpoint

### `POST /predict`

Recebe um JSON com os campos brutos da notificação e retorna a predição do modelo.

**Exemplo de requisição:**

```json
{
  "IDADE_ANOS": 23,
  "VIOL_FISIC": 1,
  "VIOL_PSICO": 1,
  "VIOL_TORT": 2,
  "VIOL_FINAN": 2,
  "VIOL_NEGLI": 2,
  "VIOL_INFAN": 2,
  "VIOL_LEGAL": 2,
  "VIOL_OUTR": 2,
  "LES_AUTOP": 2,
  "AUTOR_ALCO": 1,
  "OUT_VEZES": 1,
  "CS_GESTANT": 5,
  "CS_RACA": 4,
  "CS_ESCOL_N": 3,
  "LOCAL_OCOR": 1,
  "AUTOR_SEXO": 1
}
```

**Exemplo de resposta:**

```json
{
  "probabilidade_viol_sexual": 0.8523,
  "classificacao": "violencia_sexual",
  "alerta": true
}
```

### Campos de entrada

| Campo | Tipo | Valores aceitos |
|---|---|---|
| IDADE_ANOS | Numérico | 0–125 |
| VIOL_FISIC, VIOL_PSICO, VIOL_TORT, VIOL_FINAN, VIOL_NEGLI, VIOL_INFAN, VIOL_LEGAL, VIOL_OUTR | Binário | 1=Sim · 2=Não · 9/ausente=Ignorado |
| LES_AUTOP | Binário | 1=Sim · 2=Não · 9/ausente=Ignorado |
| AUTOR_ALCO | Binário | 1=Sim · 2=Não · 9/ausente=Ignorado |
| OUT_VEZES | Binário | 1=Sim · 2=Não · 9/ausente=Ignorado |
| CS_GESTANT | Categórico | 1=1º tri · 2=2º tri · 3=3º tri · 4=Idade gestacional ignorada · 5=Não gestante · 6=Não se aplica · 8=Não informado |
| CS_RACA | Categórico | 1=Branca · 2=Preta · 3=Amarela · 4=Parda · 5=Indígena |
| CS_ESCOL_N | Categórico | 0=Sem escol. · 1=Fund. I incomp. · 2=Fund. I comp. · 3=Fund. II incomp. · 4=Fund. II comp. · 5=Médio incomp. · 6=Médio comp. · 7=Superior incomp. · 8=Superior comp. · 10=Não informado |
| LOCAL_OCOR | Categórico | 1=Residência · 2=Hab. coletiva · 3=Escola · 4=Esporte · 5=Bar/Boate · 6=Via pública · 7=Comércio · 8=Indústria |
| AUTOR_SEXO | Categórico | 1=Masculino · 2=Feminino · 3=Ambos · 4=Ignorado |

### Campos de saída

| Campo | Tipo | Significado |
|---|---|---|
| probabilidade_viol_sexual | float (0–1) | Probabilidade estimada de violência sexual |
| classificacao | string | "violencia_sexual" ou "sem_violencia_sexual" |
| alerta | bool | true se prob ≥ 0.5 (threshold padrão) |

