# Agente 03 - Planejador de Plataforma e Observabilidade

## Missão

Planejar Docker, Compose, configuração, health checks, logs, CI e operação local.

## Cobertura

- AT-03, AT-17 a AT-20 e AT-27 a AT-29;
- SDD seções 8, 17, 18, 20 e 22;
- CT-HEALTH, CT-OBS, CT-DOCKER e CT-PERF.

## Propriedade planejada

- `Dockerfile`;
- `compose.yaml`;
- `.dockerignore`;
- `.env.example`;
- pipeline CI;
- scripts operacionais;
- execução e troubleshooting do README.

Mudanças em `app/**` exigem handoff com Backend.

## Entregas do plano

1. Dockerfile não root com Gunicorn.
2. Serviços `db`, `migrate` e `api`.
3. Health checks e ordem de inicialização.
4. Volume e rede interna.
5. Variáveis e defaults seguros.
6. Pool, timeouts e limite de 64 KiB.
7. Logs JSON e request ID sem payload.
8. Encerramento gracioso.
9. Etapas do pipeline em ordem.
10. Smoke test e teste de desempenho.

## Verificações planejadas

- build sem cache;
- Compose em ambiente vazio;
- migration e seed concluídos;
- reinício sem duplicação;
- persistência do volume;
- liveness/readiness com banco disponível e indisponível;
- usuário não root;
- ausência de secrets e payload nos logs;
- p95 conforme o SDD.

## Perguntas obrigatórias

- Como o job migrate sinaliza conclusão?
- Qual comando inicia Gunicorn?
- Como o CI fornece PostgreSQL?
- Quais scanners serão adotados?
- Qual ambiente e massa medirão desempenho?

## Saída

`plano-plataforma-observabilidade.md` preenchido pelo template global.
