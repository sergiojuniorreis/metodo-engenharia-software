# §8 — Estado, concorrência e memória

## Classifique antes de escolher a técnica

| Categoria | Estratégia |
|---|---|
| Estado compartilhado mesclável | Revisão verificável + escrita condicional |
| Imutável por chave | Primeiro a chegar vale |
| Eventos append-only | Partição por origem e período |
| Estado exclusivo da máquina | Fica local, não sincroniza |

## Concorrência e recuperação

- **Ler → mesclar → gravar não é atômico.** Envie a revisão esperada; divergiu, o servidor
  responde **conflito explícito e não grava**; o cliente relê, remescla e repete com limite.
- **Nada de contador global** regravado por várias origens: partição por origem e período,
  agregação na leitura, sem contar o mesmo evento duas vezes.
- **Chave de idempotência estável por operação**, derivada de identificadores reais, sem dado
  sensível em claro.
- **Máquina de estados explícita:** `pendente`, `em_execucao`, `confirmada`,
  `ambigua_requer_verificacao`, `falhou`, `cancelada_por_regra`. Transição registrada com
  data, tentativa e evidência.
- **Ambíguo por timeout vira `ambigua_requer_verificacao`** — verifique o estado real antes de
  repetir; nunca reexecute no escuro.
- **Teste de retomada nos cinco cortes:** antes de enviar; após enviar e antes da resposta;
  após a resposta e antes do checkpoint; durante migração; durante conflito de sincronização.
- **Retenção e compactação definidas desde o início**: evento bruto arquiva, agregado fica
  para consulta rápida.

## Memória do sistema

1. **Camada de verdade é uma só**, fora da máquina. O local é espelho; em divergência a
   máquina reconcilia com a fonte, nunca o contrário.
2. **Memória é cache de decisão, não fonte de verdade.** Perdê-la inteira custa tempo e
   dinheiro de IA; não pode mudar o que o sistema considera certo.
3. **Toda entrada carrega quatro colunas:** origem, data, **versão da regra que a criou** e
   TTL. Faltou uma, não entra.
4. **Mudou a regra, invalida em cascata.** Subiu a versão da skill, da regra ou do modelo, o
   que ela produziu é reavaliado — não se herda decisão tomada sob outra régua. É isso que
   impede a memória de brigar com regra, tabela ou catálogo novo.
5. **Lápide é invalidação explícita e propagada:** o erro esquecido uma vez fica registrado
   *como esquecido*, para que nenhuma máquina o ressuscite na sincronização seguinte.
6. **Teto de tamanho com descarte por regra.** Memória que satura e despeja pelo fim da fila
   joga fora justamente o histórico bom.
7. **Memória auditável:** dá para perguntar por que uma decisão foi tomada e chegar à entrada
   que a causou, com data e origem.

## TTL: dimensionado por projeto, nunca herdado

**Não existe TTL padrão.** Calcule pelo **menor** entre dois prazos:

- em quanto tempo o fato pode mudar (catálogo, preço, regra do órgão, contrato do fornecedor);
- em quanto tempo perceberíamos que a entrada envelheceu errada.

| Dimensão do projeto | TTL típico | Razão |
|---|---|---|
| Base externa muda toda semana; erro caro (preço, disponibilidade, prazo) | Horas a poucos dias | A memória envelhece mais rápido do que rende |
| Regra estável, revisitada a cada execução, erro barato de corrigir | 30 a 90 dias | O fato muda devagar e o erro se corrige na execução seguinte |
| Fato imutável por natureza (OCR de um documento, hash de arquivo) | Sem TTL — imutável por chave | Data não tem o que invalidar |
| Recomputar é caro e a mudança é sinalizada por versão | Vence por versão, não por data | A invalidação em cascata substitui o relógio |
| Volume alto com custo de IA relevante por entrada | O maior TTL que a taxa de acerto sustentar | Encurtar TTL aqui é devolver conta de IA |

Regras que valem para qualquer TTL escolhido:

- **Escreva o número e a razão** junto da política de memória; TTL sem razão escrita é chute
  que ninguém revisa.
- **Meça antes de mexer:** taxa de acerto da memória, idade média da entrada usada e quantos
  erros vieram de entrada vencida. Ajuste por medição, não por sensação.
- **Volume decide junto com o relógio:** se a memória satura antes do TTL, o teto e a política
  de descarte mandam — e o descarte sai por regra, nunca por acidente.
- **Curto demais devolve custo de IA; longo demais decide com informação velha.** Os dois se
  medem, e o número se revisa quando o projeto muda de tamanho.
