# Exemplo — estudo de abordagem de um projeto grande

Projeto **fictício** para mostrar o `/estudo` no porte grande. Os números são inventados para o
exemplo; num projeto real, número que não se tem é "a medir".

**Pedido:** "Quero uma plataforma de agendamento para clínicas: várias clínicas, agenda por
profissional, lembrete por WhatsApp e cobrança da consulta por Pix."

## 0. Porte

**Grande** — várias empresas (clínicas) no mesmo sistema, dado pessoal e de saúde, dinheiro
(cobrança), integração com terceiros (mensageria, pagamento).

## 1. Problema

Clínicas pequenas perdem consultas por falta e cobram na mão; o número que mostra a melhora é a
taxa de falta por mês e o tempo entre consulta e pagamento recebido.

## 2. As oito perguntas (resumo)

| # | Resposta |
|---|---|
| 1 | Existem produtos prontos; o diferencial pedido é Pix integrado e preço para clínica pequena. **Decisão do dono:** construir |
| 2 | Servidor nosso (API + painel web); celular da recepção só pelo navegador |
| 3 | I/O e espera (mensageria, pagamento); pouca CPU; serviço de pé com pessoa esperando |
| 4 | 50 clínicas e 3 mil consultas/dia no primeiro ano (fictício); pico às 8h; resposta do painel < 300 ms p95 |
| 5 | O próprio dono, sozinho → uma linguagem, um banco, deploy simples |
| 6 | Uma via: modelo de dados multiempresa, provedor de pagamento, contrato de webhook |
| 7 | Lembrete que não sai = falta; cobrança duplicada = dinheiro devolvido e cliente perdido |
| 8 | Gatilhos: dado de mais de um dono, dado pessoal sensível (saúde), pagamento, webhook de fora, login |

## 3. Requisitos não funcionais (fictícios)

| Requisito | Alvo |
|---|---|
| Disponibilidade do agendamento | 99,5% no mês |
| RPO / RTO | 15 min / 4 h |
| Retenção | Prontuário fora do escopo; agenda 5 anos (a confirmar com o dono e a lei) |

## 4. Pre-mortem

| Falhou porque… | Saída |
|---|---|
| Uma clínica viu agenda de outra | Coluna de clínica em toda tabela e índice; teste de isolamento A grava, B não vê (§14.6 item 2) |
| Pix cobrado duas vezes no reenvio do webhook | Chave de idempotência por cobrança; webhook idempotente com deduplicação (§3D, §8) |
| Lembrete parou e ninguém percebeu | Métrica de lembretes enviados por hora com alerta de queda (§9) |

## 5. Ameaças (recorte)

| Elemento | Ameaça | Item ou teste |
|---|---|---|
| Webhook do pagamento | Falsificação (S), repetição | Assinatura conferida; idempotência; item 10 |
| Painel | Acesso entre clínicas (I, E) | Autorização por recurso no servidor; item 11 e item 2 |
| Mensagem ao paciente | Dado de saúde no texto | Texto sem diagnóstico; §11 |

## 6. As quatro análises

- **A:** não se aplica — sem IA na primeira versão.
- **B:** não se aplica.
- **C:** fluxo não linear: agendamento → confirmado → lembrado → atendido / faltou / cancelado;
  cobrança → pendente → paga / expirada / estornada. Máquinas de estado escritas, cada transição
  com teste.
- **D:** lembrete agendado (fuso, execução dupla), webhook do pagamento ("pelo menos uma vez" →
  consumidor idempotente), envio de mensagem (fila com teto e fila morta). Outbox para "cobrança
  criada → avisar".

## 7. Desenho mínimo

Um serviço (monólito modular: agenda, cobrança, mensagens), um PostgreSQL, uma tabela de tarefas
com um worker para lembretes e webhooks. **Sem** fila externa, cache distribuído nem
microsserviços até um número medido pedir (§10).

## 8. ADRs

| ADR | Decisão |
|---|---|
| 0002 | Multiempresa por coluna de clínica + teste de isolamento, não banco por clínica |
| 0003 | Provedor de Pix: <a decidir pelo dono> |
| 0004 | Tarefas agendadas em tabela + worker, não fila externa |

## 9. Fatias

| Fatia | Caminho de ponta a ponta |
|---|---|
| 1 | Uma clínica cria um horário e um paciente agenda — com login, isolamento testado, log e deploy |
| 2 | Lembrete agendado sai pelo provedor de mensagem, com idempotência e alerta de queda |
| 3 | Cobrança Pix criada no agendamento, webhook idempotente, estado da cobrança no painel |

## 10. Para o dono decidir

- Provedor de Pix (custo por transação × qualidade do webhook) — ADR 0003.
- Retenção da agenda: 5 anos é suposição; confirmar com a lei aplicável e o contador.
- Lembrete por WhatsApp exige conta comercial e modelo de mensagem aprovado: quem cuida?
