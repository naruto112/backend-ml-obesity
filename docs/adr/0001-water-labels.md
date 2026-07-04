# ADR 0001 - Rotulos do dominio litro_agua

## Status

Provisorio para ambiente local e academico.

## Decisao

O seed usa os rotulos propostos no refinamento tecnico: `1` Ate 1 L,
`2` Entre 1-2 L e `3` Mais de 2 L/dia. Os codigos fazem parte do contrato v1.

## Consequencias

Uma alteracao futura de rotulos pode ser feita pelo seed idempotente. Uma alteracao
de codigos exige migration de dados e decisao de versionamento. A publicacao em
producao permanece bloqueada ate a confirmacao dos rotulos pelo responsavel.
