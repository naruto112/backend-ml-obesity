# Plano de implementacao consolidado

## Identificacao

- Orquestrador: Agente 00
- Agentes consultados: Backend Flask, Dados PostgreSQL, QA e Seguranca
- Data: 2026-07-03
- Fonte: `specs-sdd.md` e `refinamento-tecnico.md`

## Fases e propriedade

| Fase | AT | Responsavel | Entrega |
|---|---|---|---|
| Fundacao | AT-01 a AT-04 | Backend | factory, config, extensoes e dependencias |
| Dados | AT-05 a AT-08 | Dados | models, migration, seed e repositories |
| Validacao | AT-09 a AT-11 | Backend | schemas estritos e services transacionais |
| API | AT-12 a AT-16 | Backend | rotas, problem details, saude e OpenAPI |
| Operacao | AT-17 a AT-20 | Plataforma | imagem, Compose, logs e limites |
| Qualidade | AT-21 a AT-28 | QA/Security | testes, cobertura e gates |
| Entrega | AT-29 e AT-30 | Orquestrador | README, ADR e evidencias |

## Decisoes

- Preservar os 13 nomes e o literal `somentimes`.
- UUID malformado retorna 400.
- Request ID aceito por `[A-Za-z0-9._:-]{1,128}`; invalido e substituido.
- Repositories constroem models para preservar `services -> repositories`.
- Rotulos de agua seguem provisoriamente PN-02; ver ADR 0001.
- PostgreSQL real e obrigatorio para integracao; SQLite e proibido.

## Gates

1. Ruff, format e mypy sem achados.
2. Cobertura geral minima de 90% e regras de dominio em 100%.
3. Migration upgrade/downgrade/upgrade em banco vazio.
4. Seed executado duas vezes sem duplicar.
5. OpenAPI e rotas consistentes.
6. Compose sobe com job `migrate` concluido antes da API.
7. Nenhum payload, segredo, URL de banco ou stack em resposta/log.
8. Achado Alto ou Critico sem mitigacao bloqueia aceite.

## Riscos residuais

- PN-02 depende da confirmacao definitiva dos rotulos de agua.
- Producao publica depende de identidade, consentimento, retencao, TLS e backup.
- Teste de desempenho exige ambiente dedicado e fica fora do smoke local.
