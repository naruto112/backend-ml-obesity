# Obesity Data API

API Flask/PostgreSQL para consultar 12 dominios e cadastrar registros de
obesidade com **predicao automatica via Machine Learning** (HistGradientBoostingClassifier).

O cliente envia os 12 campos do formulario e a API prediz a classe de obesidade
server-side antes de persistir o registro (13 campos no banco).

## Arquitetura ML

```
POST /api/v1/obesity-records (12 campos)
  │
  ├─ Validacao (schema 12 inputs)
  ├─ FeatureTransformer (12 inputs → 15 features)
  ├─ ObesityPredictor (model.predict → classe)
  └─ Persistencia (12 inputs + obesity predito)
```

### Pipeline de inferencia (`app/ml/`)

| Modulo | Responsabilidade |
|--------|-----------------|
| `feature_transformer.py` | Transforma os 12 campos da API em DataFrame com 15 features (ordinal encoding, one-hot, MTRANS dummies) |
| `model_loader.py` | Verifica integridade do artefato (SHA-256 + tamanho) e carrega o modelo |
| `predictor.py` | Orquestra transformacao + predicao + mapeamento codigo→classe |

### Artefato do modelo

- Arquivo: `artifacts/hgb.joblib` (HistGradientBoostingClassifier)
- Manifesto: `artifacts/hgb.manifest.json` (SHA-256, features, classes)
- Verificacao: `python scripts/verify_model_artifact.py artifacts/hgb.manifest.json`
- Gerar/atualizar manifesto: `python scripts/generate_model_manifest.py artifacts/hgb.joblib`
  (extrai SHA-256, tamanho, algoritmo, features e versao do sklearn do modelo;
  reaproveita `version`, `class_map` e `provenance` do manifesto existente. Use
  `-` como destino para imprimir sem gravar. Sempre revise os campos marcados
  com `TODO` antes de commitar.)

> Trocou o `.joblib`? O `hgb.manifest.json` fixa o hash/tamanho do artefato,
> entao a API falha com `SHA-256 mismatch` ate o manifesto ser regenerado.
> Rode o gerador acima e confira se as `features` do novo modelo batem com as
> produzidas por `feature_transformer.py`.

### Classes preditas

| Codigo | Classe |
|--------|--------|
| 0 | Insufficient_Weight |
| 1 | Normal_Weight |
| 2 | Obesity_Type_I |
| 3 | Obesity_Type_II |
| 4 | Obesity_Type_III |
| 5 | Overweight_Level_I |
| 6 | Overweight_Level_II |

### Transformacao de features (12 → 15)

| Feature | Campo API | Transformacao |
|---------|-----------|---------------|
| Age | idade | direto |
| FCVC | come_vegetaiis | direto |
| NCP | refeicoes_diariamente | direto |
| CAEC | come_entre_refeicao | ordinal (no=0, somentimes=1, frequently=2, always=3) |
| CH2O | litro_agua | direto |
| FAF | frequencia_semanal_atvidade_fisica | direto |
| TUE | horas_dispositivo_eletronico | direto |
| CALC | consome_bebida_alcoolica | ordinal |
| Gender_Male | sexo_biologico | 1 se masculino(1), 0 se feminino(2) |
| family_history_yes | historico_familiar | 1 se "yes", 0 se "no" |
| FAVC_yes | alimentos_calorico | 1 se "yes", 0 se "no" |
| MTRANS_Bike | meio_transporte | one-hot (automobile e referencia = zeros) |
| MTRANS_Motorbike | meio_transporte | one-hot |
| MTRANS_Public_Transportation | meio_transporte | one-hot |
| MTRANS_Walking | meio_transporte | one-hot |

## Executar com Docker

Crie `.env` a partir de `.env.example`, substitua `change-me` por uma senha local
e mantenha a mesma credencial em `DATABASE_URL`. Depois execute:

```powershell
docker compose up --build
```

A API fica em `http://localhost:8000`, o Swagger em `/api/docs` e o documento
OpenAPI em `/api/openapi.json`. O PostgreSQL nao publica porta no host.

### Variaveis de ambiente ML

| Variavel | Default | Descricao |
|----------|---------|-----------|
| `ML_MODEL_PATH` | `artifacts/hgb.joblib` | Caminho do modelo serializado |
| `ML_MANIFEST_PATH` | `artifacts/hgb.manifest.json` | Caminho do manifesto de verificacao |

## Desenvolvimento

Requer Python >=3.10 e PostgreSQL. Com `APP_ENV` e `DATABASE_URL` configurados:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\alembic.exe upgrade head
.\.venv\Scripts\python.exe -m seeds.domain_options
.\.venv\Scripts\python.exe -m pytest --cov=app
```

Qualidade:

```powershell
.\.venv\Scripts\python.exe -m ruff check app seeds migrations tests scripts
.\.venv\Scripts\python.exe -m ruff format --check app seeds migrations tests scripts
.\.venv\Scripts\python.exe -m mypy app seeds scripts
```

### Falha ao rodar o migrate localmente

Se o projeto nao rodar localmente e o `alembic upgrade head` (migrate) falhar,
suba manualmente o schema executando o script SQL em
`migrations/versions/script.sql` direto no banco de dados. Exemplo com `psql`:

```powershell
psql "$env:DATABASE_URL" -f migrations/versions/script.sql
```

## Rotas

- `GET /health/live` e `GET /health/ready`
- `GET /api/v1/domains` e `GET /api/v1/domains/{field_name}`
- `POST /api/v1/obesity-records` — aceita 12 campos, retorna 13 (com `obesity` predito)
- `GET /api/v1/obesity-records` — lista todos os registros
- `GET /api/v1/obesity-records/{id}`

### Contrato POST /api/v1/obesity-records

**Request (12 campos):**

```json
{
  "idade": 25,
  "sexo_biologico": 1,
  "come_vegetaiis": 2,
  "refeicoes_diariamente": 3,
  "come_entre_refeicao": "somentimes",
  "litro_agua": 2,
  "frequencia_semanal_atvidade_fisica": 1,
  "horas_dispositivo_eletronico": 1,
  "consome_bebida_alcoolica": "no",
  "historico_familiar": "yes",
  "alimentos_calorico": "no",
  "meio_transporte": "public_transportation"
}
```

**Response (13 campos — obesity predito pelo modelo):**

```json
{
  "id": "uuid",
  "created_at": "2026-07-04T18:00:00Z",
  "idade": 25,
  "obesity": "Normal_Weight",
  "..."
}
```

> Se o campo `obesity` for enviado no payload, a API retorna `422 unknown_field`.

Erros usam `application/problem+json`. Toda resposta inclui `X-Request-ID`.
Payloads e campos de saude nao sao registrados nos logs.

## Limites de uso

Esta versao e local/academica. Exposicao publica esta bloqueada ate definir
autenticacao, autorizacao, consentimento, retencao, descarte, TLS, CORS, backup
e politica de acesso a respostas por UUID.
