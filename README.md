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

- Python **≥ 3.11** (testado com 3.12, 3.13 e 3.14 — veja a [seção de compatibilidade](#compatibilidade-de-versões-do-python))
- Arquivos de modelo em `model/` (gerados pelo pipeline de treino):
  - `xgb_viol_sexu.joblib`
  - `imputer.joblib`
  - `feature_columns.joblib`

## Instalação

```bash
pip install -r requirements.txt
```

## Compatibilidade de versões do Python

As versões mínimas exigidas pelos pacotes do `requirements.txt` são:

| Pacote | Versão no arquivo | Python mínimo | Wheels prontas para |
|---|---|---|---|
| `numpy` | 2.4.4 | ≥ 3.11 | 3.11, 3.12, 3.13, 3.14 |
| `pandas` | 3.0.2 | ≥ 3.11 | 3.11, 3.12, 3.13, 3.14 |
| `scipy` | 1.17.1 | ≥ 3.11 | 3.11, 3.12, 3.13, 3.14 |
| `scikit-learn` | 1.8.0 | ≥ 3.11 | 3.11, 3.12, 3.13, 3.14 |
| `shap` | 0.51.0 | ≥ 3.11 | 3.11, 3.12, 3.13, 3.14 |
| `llvmlite` | 0.47.0 | ≥ 3.10 | 3.10, 3.11, 3.12, 3.13, 3.14 |
| `numba` | 0.65.1 | ≥ 3.10 | 3.10, 3.11, 3.12, 3.13, 3.14 |
| `cffi` | 2.0.0 | ≥ 3.9 | 3.9 … 3.14 |
| `xgboost` | 2.1.4 | ≥ 3.8 | 3.8 … 3.14 |

> **Conclusão:** o `requirements.txt` funciona com **Python 3.11, 3.12, 3.13 e 3.14**.  
> Python 3.10 ou inferior causará falha na instalação de `numpy`, `pandas`, `scipy`, `scikit-learn` e `shap`.

### Plataformas testadas

Todos os pacotes acima disponibilizam *wheels* pré-compiladas para **Windows (x86-64)**, **macOS (Intel e Apple Silicon)** e **Linux (x86-64)**. Portanto, o `pip install -r requirements.txt` não exige compilador C/C++ nas plataformas mais comuns.

---

## Resolução de problemas comuns

### ❌ `ERROR: Package X requires Python >=3.11`

**Causa:** versão do Python instalada é inferior à 3.11.

**Solução:**
1. Verifique a versão atual: `python --version` ou `python3 --version`
2. Instale o Python 3.12 ou 3.13 em [python.org/downloads](https://www.python.org/downloads/)
3. No Windows, durante a instalação marque a opção **"Add Python to PATH"**
4. Crie um novo ambiente virtual e reinstale:
   ```bash
   python3.12 -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS / Linux:
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

---

### ❌ `pip` instala com a versão Python errada (Windows)

**Causa:** o `pip` no PATH pertence a uma instalação antiga do Python.

**Solução:** use sempre `python -m pip` vinculado ao interpretador correto:
```bash
python3.12 -m pip install -r requirements.txt
```

---

### ❌ `Microsoft Visual C++ 14.0 or greater is required` (Windows)

**Causa:** algum pacote não encontrou *wheel* pré-compilada e tentou compilar código C.  
Isso **não deve ocorrer** com as versões do `requirements.txt` em Python 3.11–3.14, mas pode acontecer se a versão do Python for incompatível.

**Solução:**
1. Confirme que está usando Python 3.11, 3.12 ou 3.13 (onde há wheels disponíveis).
2. Se ainda for necessário compilar, instale o **Build Tools for Visual Studio**:  
   [visualstudio.microsoft.com/visual-cpp-build-tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)  
   Selecione a carga de trabalho **"Desenvolvimento para desktop com C++"**.

---

### ❌ `xcrun: error: invalid active developer path` (macOS)

**Causa:** Xcode Command Line Tools não está instalado.

**Solução:**
```bash
xcode-select --install
```

---

### ❌ `ERROR: Could not find a version that satisfies the requirement X==Y.Y.Y`

**Causa:** versão exata do pacote não está disponível para a combinação Python + sistema operacional.

**Solução:** tente instalar sem fixar a versão para verificar qual é compatível:
```bash
pip install <nome-do-pacote>
```
Em seguida, atualize o número de versão no `requirements.txt` se necessário.

---

### ❌ `pip` não encontra o `requirements.txt`

**Causa:** o comando foi executado em um diretório diferente da raiz do projeto.

**Solução:**
```bash
# Navegue até a pasta raiz do projeto clonado
cd Fiap_Pos_9AIDT_Fase_01_API
pip install -r requirements.txt
```

---

### ⚠️ `pywinpty` não encontrado (Windows)

O arquivo `requirements.txt` não lista `pywinpty` explicitamente, mas o pacote `terminado` — necessário para o Jupyter — declara `pywinpty>=1.1.0` como dependência condicional para Windows. O `pip` instala `pywinpty` automaticamente; nenhuma ação manual é necessária.

---

### ⚠️ `jupyter` ou `notebook` não abre no macOS com Apple Silicon (M1/M2/M3)

**Causa:** alguns pacotes legados não têm wheel nativa para `arm64`.

**Solução:** garanta que está usando Python instalado via [python.org](https://www.python.org/downloads/macos/) (Universal2) ou via [Homebrew](https://brew.sh):
```bash
brew install python@3.12
python3.12 -m venv .venv
source .venv/bin/activate
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

## Instalação via Docker Compose

### Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) instalado (versão 20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) instalado (versão 2.0+ ou plugin `docker compose`)
- Arquivos de modelo presentes na pasta `model/` do projeto:
  - `xgb_viol_sexu.joblib`
  - `imputer.joblib`
  - `feature_columns.joblib`

### Passo a passo

**1. Clone o repositório**

```bash
git clone https://github.com/Etyonamine/Fiap_Pos_9AIDT_Fase_01_API.git
cd Fiap_Pos_9AIDT_Fase_01_API
```

**2. Adicione os arquivos de modelo**

Copie os arquivos do modelo treinado para a pasta `model/` na raiz do projeto:

```
model/
├── xgb_viol_sexu.joblib
├── imputer.joblib
└── feature_columns.joblib
```

**3. Construa a imagem e suba o container**

```bash
docker compose up --build
```

> Na primeira execução o Docker irá baixar a imagem base (`python:3.14-slim`) e instalar as dependências. As execuções seguintes serão mais rápidas pois o cache de camadas é reutilizado.

**4. Verifique se o serviço está em execução**

```bash
docker compose ps
```

A saída esperada mostra o container `fiap_fase01_api` com status `running` e a porta `5000` exposta.

**5. Acesse a API**

| Recurso | URL |
|---|---|
| Endpoint de predição | `http://localhost:5000/predict` |
| Documentação Swagger | `http://localhost:5000/docs/` |

**6. (Opcional) Executar em segundo plano**

Para rodar o serviço em modo *detached* (sem bloquear o terminal):

```bash
docker compose up --build -d
```

**7. Parar o serviço**

```bash
docker compose down
```

Para parar e remover também os volumes criados:

```bash
docker compose down -v
```

