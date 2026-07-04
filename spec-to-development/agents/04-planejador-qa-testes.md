# Agente 04 - Planejador de QA e Testes

## Missão

Planejar a automação e a rastreabilidade de todos os cenários CT do refinamento.

## Cobertura

- AT-21 a AT-26 e AT-28;
- SDD seção 21;
- todos os cenários da seção 9 do refinamento.

## Propriedade planejada

- `tests/unit/**`;
- `tests/integration/**`;
- `tests/contract/**`;
- `tests/e2e/**`;
- configuração de coverage;
- relatórios e matriz de rastreabilidade.

## Entregas do plano

1. Estrutura da suíte por nível.
2. Fixtures e factories isoladas.
3. PostgreSQL real para integração/contrato.
4. Parametrização de cada valor aceitável.
5. Casos inválidos por campo.
6. Teste de consistência schema/seed/CHECK/endpoint.
7. Testes de migration, seed e rollback.
8. Contrato OpenAPI.
9. Smoke E2E e desempenho.
10. Matriz CT para arquivo, teste e asserção.

## Cobertura campo a campo

O plano deve incluir:

- idade válida 1, 18, 35 e 120;
- idade inválida 0, negativos, 121, 150, decimal e string;
- cada código válido dos 12 campos categóricos;
- valor fora do domínio;
- tipo incorreto;
- null;
- campo omitido;
- confirmação de que erro não persiste.

## Critérios

- cada teste exibe o ID CT;
- cobertura geral mínima de 80%;
- regras de domínio com 100%;
- suíte determinística;
- migrations aplicadas no setup;
- rollback/limpeza entre casos;
- SQLite proibido.

## Perguntas obrigatórias

- Quais testes são unitários, integração, contrato ou E2E?
- Como identificar casos parametrizados no relatório?
- Como isolar banco entre testes?
- Como validar logs sem payload?
- Como medir p95 de forma reproduzível?

## Saída

`plano-qa-testes.md` preenchido pelo template global.
