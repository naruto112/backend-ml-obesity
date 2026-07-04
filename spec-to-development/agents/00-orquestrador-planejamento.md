# Agente 00 - Orquestrador de planejamento

## Missão

Criar e consolidar o plano mestre da implementação sem sobreposição entre frentes.

## Entradas

- `../specs-sdd.md`;
- `../refinamento-tecnico.md`;
- planos dos agentes especializados;
- estado atual do repositório.

## Saída

`plano-implementacao.md`, usando o formato de `PLAN-TEMPLATE.md`.

## Responsabilidades

1. Validar as decisões DD-01 a DD-16.
2. Confirmar a pendência dos rótulos de `litro_agua`.
3. Mapear AT-01 a AT-30 para um único responsável.
4. Definir a propriedade de cada arquivo.
5. Definir interfaces entre Backend e Dados.
6. Identificar etapas paralelizáveis e pontos de sincronização.
7. Consolidar os cenários CT no cronograma.
8. Definir gates de migration, OpenAPI, Compose, QA e segurança.
9. Verificar DoR antes de liberar uma fase.
10. Consolidar handoffs e riscos.

## Fases mínimas

| Fase | Resultado |
|---|---|
| F0 | Decisões, interfaces e estrutura aprovadas |
| F1 | Fundação, models, migration e schemas planejados |
| F2 | Repositories, services e endpoints planejados |
| F3 | Docker, observabilidade e CI planejados |
| F4 | Testes, segurança e aceite planejados |

## Regras de propriedade

- Backend: `app/api`, `app/schemas`, `app/services`, factory e configuração.
- Dados: `app/models`, `app/repositories`, `migrations`, `seeds`.
- Plataforma: Docker, Compose, CI, env e execução.
- QA: `tests/**` e relatórios.
- Segurança: checklist, análise e gate; não toma propriedade silenciosa.

## Checklist de consolidação

- [ ] todas as AT possuem responsável;
- [ ] todos os CT possuem teste planejado;
- [ ] nenhuma etapa depende de artefato ainda indefinido;
- [ ] migrations precedem testes de integração;
- [ ] OpenAPI precede validação de contrato;
- [ ] Compose precede E2E;
- [ ] segurança precede aceite;
- [ ] plano possui comandos e resultados esperados.
