# Agente 01 - Planejador Backend Flask

## Missão

Planejar a implementação da aplicação Flask, schemas, services, rotas, erros e OpenAPI.

## Cobertura

- AT-01, AT-02 e AT-09 a AT-16;
- SDD seções 5 a 13;
- CT de validação, API, contrato e saúde.

## Propriedade planejada

- `app/__init__.py`;
- `app/config.py`;
- `app/extensions.py`;
- `app/api/**`;
- `app/schemas/**`;
- `app/services/**`;
- `wsgi.py`;
- dependências de aplicação no `pyproject.toml`.

Models, repositories, migrations e seeds pertencem ao plano de Dados.

## Entregas do plano

1. Sequência para application factory e blueprints.
2. Escolha documentada de biblioteca de schemas/OpenAPI.
3. Schemas estritos para os 13 campos.
4. Mapeamento dos códigos de validação.
5. Interfaces de DTOs, services e repositories.
6. Rotas, status, headers e exemplos.
7. Middleware de erros e request ID.
8. Estratégia de liveness e readiness.
9. Testes unitários e de contrato previstos.
10. Comandos de verificação.

## Decisões que o plano deve preservar

- idade de 1 a 120;
- campos obrigatórios, não nulos e sem extras;
- inteiros sem coerção de strings;
- nomes/literais da v1;
- POST com 201, UUID e Location;
- erros problem+json;
- liveness sem SQL e readiness com SQL;
- nenhum payload nos logs.

## Interface com Dados

O plano deve definir antes da implementação:

```python
DomainRepository.list_active_with_options()
DomainRepository.get_active_by_name(name)
ObesityRecordRepository.add(record)
ObesityRecordRepository.get_by_id(record_id)
```

Também deve definir DTOs e responsabilidade de commit/rollback.

## Perguntas obrigatórias

- Qual biblioteca garantirá tipos estritos?
- Como evitar divergência entre schema, seed e CHECK?
- Qual status será usado para UUID malformado?
- Como o OpenAPI será gerado e validado?
- Como request ID será validado?

## Saída

`plano-backend-flask.md` preenchido pelo template global.
