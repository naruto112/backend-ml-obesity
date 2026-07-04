# Regras globais dos agentes de planejamento

## Fonte de verdade

Cada agente deve ler integralmente:

1. `../specs-sdd.md`;
2. `../refinamento-tecnico.md`;
3. este arquivo.

A Specs SDD define o desenho. O refinamento define requisitos e cenários de aceite.

## Finalidade

Estes agentes planejam implementações. Eles não implementam código durante a etapa de planejamento.

## Regras obrigatórias

- Preservar os 13 campos e os domínios da API v1.
- Manter idade entre 1 e 120, inclusive.
- Preservar os nomes com erro ortográfico e o literal `somentimes`.
- Não criar endpoints, tabelas ou dependências ausentes do SDD sem registrar proposta.
- PostgreSQL é obrigatório para integração.
- Payload e dados relacionados à saúde não podem aparecer em logs.
- Toda atividade deve apontar arquivos, dependências, testes e critério de conclusão.
- Planos não podem atribuir o mesmo arquivo a agentes diferentes sem handoff.
- Dúvidas que alterem contrato devem ser classificadas como bloqueio.
- Nenhum plano pode declarar uma atividade pronta sem DoR verificável.

## Formato obrigatório de saída

Todo agente deve usar `PLAN-TEMPLATE.md` e produzir:

- objetivo;
- escopo incluído e excluído;
- atividades AT e cenários CT cobertos;
- inventário de arquivos;
- interfaces e contratos afetados;
- passos pequenos e ordenados;
- dependências e paralelismo permitido;
- comandos de verificação;
- riscos e rollback;
- DoR, DoD e handoff.

## Prioridade de decisão

1. decisão explícita mais recente do responsável;
2. Specs SDD;
3. refinamento técnico;
4. código existente.

## Proibições

- não implementar durante o planejamento;
- não alterar silenciosamente o contrato;
- não esconder pendências;
- não usar termos como "testar tudo" sem listar o que será testado;
- não usar SQLite como substituto do PostgreSQL;
- não planejar migrations executadas por cada worker web.
