# Estudo de abordagem — <projeto>

Modelo do §3. Preencha no porte declarado; o que não se aplica diz "não se aplica — motivo".
Campo sem resposta do dono fica **"a decidir: <pergunta>"** — nunca suposto em silêncio.

## 0. Porte

**<script · pequeno · grande>** — motivo: <…>

## 1. Problema

<Uma frase: o problema, quem sente, quanto custa hoje, o número que vai mostrar que melhorou.>

## 2. As oito perguntas

| # | Pergunta | Resposta |
|---|---|---|
| 1 | Vale construir? (produto pronto, rota oficial, mudar o processo) | |
| 2 | Onde o trabalho acontece? | |
| 3 | Forma do problema (I/O ou CPU; documento ou número; pontual ou contínuo) | |
| 4 | Volume e latência, hoje e em 12 meses (em número) | |
| 5 | Quem mantém daqui a um ano? | |
| 6 | Quais decisões são de uma via? (viram ADR) | |
| 7 | O que acontece quando falhar? | |
| 8 | O que pode vazar ou ser abusado? (gatilhos da pauta §14.6) | |

## 3. Requisitos não funcionais (porte pequeno e grande)

| Requisito | Alvo | Como se mede |
|---|---|---|
| Volume / pico | | |
| Latência | | |
| Disponibilidade | | |
| RPO / RTO | | |
| Custo por unidade de trabalho | | |
| Retenção de dados | | |

## 4. Pre-mortem (pequeno: 3 causas; grande: todas as plausíveis)

| O projeto falhou porque… | Saída: mitigação no desenho, teste ou alerta | Dono |
|---|---|---|
| | | |

## 5. Ameaças (porte grande: STRIDE por elemento do fluxo de dados)

| Elemento / fronteira | Ameaça (S, T, R, I, D, E; IA: injeção, agência) | Item da pauta ou teste |
|---|---|---|
| | | |

## 6. As quatro análises do escopo

- **A. Paradigma de IA:** <simbólica · subsimbólica · híbrida · não se aplica — motivo>
- **B. Rede:** <forma do dado → família → base simples a vencer · não se aplica>
- **C. Linear ou não linear:** problema <…>; fluxo <linear · máquina de estados com transições>
- **D. Assíncronos:** <movimentos, idempotência, ordem, outbox, saga, fila morta · não se aplica>

## 7. Desenho mínimo

<Componentes e por quê — cada um com o problema medido que o justifica (§10, escada). Linguagem
por camada, com o motivo (§3). Diagrama ou lista do fluxo.>

## 8. Decisões de uma via (ADR)

| ADR | Decisão | Estado |
|---|---|---|
| 0001 | | proposta |

## 9. Fatias de entrega (porte grande)

| Fatia | Caminho de ponta a ponta | Pronto quando |
|---|---|---|
| 1 | <entrada → regra → saída, com log e teste> | |
| 2 | | |

## 10. Para o dono decidir

- <pergunta> — <opções e consequência de cada>
