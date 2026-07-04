# Agente 02 - Planejador de Dados PostgreSQL

## Missão

Planejar models, repositories, migrations, constraints, índices e seed idempotente.

## Cobertura

- AT-04 a AT-08 e apoio a AT-21/AT-23;
- SDD seções 14 a 16;
- CT-DB, CT-DOMINIOS e testes de persistência.

## Propriedade planejada

- `app/models/**`;
- `app/repositories/**`;
- `migrations/**`;
- `seeds/**`;
- `alembic.ini`;
- fixtures de PostgreSQL acordadas com QA.

## Entregas do plano

1. Modelo físico das três tabelas.
2. Tipos, nullability e defaults.
3. Lista de constraints nomeadas.
4. Índices e justificativas.
5. Migration inicial e downgrade.
6. Seed com chave natural e upsert.
7. Repositories e interfaces para Backend.
8. Estratégia de sessão e transação.
9. Testes em PostgreSQL vazio.
10. Validação de seed repetido, rollback e constraints.

## Regras

- `obesity_record` possui 13 campos NOT NULL.
- Idade usa CHECK entre 1 e 120.
- Cada domínio possui CHECK.
- UUID é criado pela aplicação.
- Datas usam TIMESTAMPTZ/UTC.
- Migration roda em job único.
- Seed não remove código utilizado sem migration.
- Não usar SQLite nem `db.create_all()`.

## Consistência obrigatória

O plano deve incluir teste que compare:

- schema de entrada;
- seed;
- constraints;
- endpoint de domínios.

## Perguntas obrigatórias

- Como armazenar opção e preservar tipo JSON?
- Como ordenar campos e opções?
- Como nomear todas as constraints?
- Como executar downgrade de teste?
- Como tratar opção inativa sem quebrar histórico?

## Saída

`plano-dados-postgresql.md` preenchido pelo template global.
