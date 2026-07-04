# Obesity Data API

API Flask/PostgreSQL para consultar 12 dominios e cadastrar os 13 campos do
formulario de obesidade definidos no contrato v1.

## Executar com Docker

Crie `.env` a partir de `.env.example`, substitua `change-me` por uma senha local
e mantenha a mesma credencial em `DATABASE_URL`. Depois execute:

```powershell
docker compose up --build
```

A API fica em `http://localhost:8000`, o Swagger em `/api/docs` e o documento
OpenAPI em `/api/openapi.json`. O PostgreSQL nao publica porta no host.

## Desenvolvimento

Requer Python 3.10 e PostgreSQL. Com `APP_ENV` e `DATABASE_URL` configurados:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\alembic.exe upgrade head
.\.venv\Scripts\python.exe -m seeds.domain_options
.\.venv\Scripts\python.exe -m pytest --cov=app
```

Qualidade:

```powershell
.\.venv\Scripts\python.exe -m ruff check app seeds migrations tests
.\.venv\Scripts\python.exe -m ruff format --check app seeds migrations tests
.\.venv\Scripts\python.exe -m mypy app seeds
```

## Rotas

- `GET /health/live` e `GET /health/ready`
- `GET /api/v1/domains` e `GET /api/v1/domains/{field_name}`
- `POST /api/v1/obesity-records`
- `GET /api/v1/obesity-records/{id}`

Erros usam `application/problem+json`. Toda resposta inclui `X-Request-ID`.
Payloads e campos de saude nao sao registrados nos logs.

## Limites de uso

Esta versao e local/academica. Exposicao publica esta bloqueada ate definir
autenticacao, autorizacao, consentimento, retencao, descarte, TLS, CORS, backup
e politica de acesso a respostas por UUID.
