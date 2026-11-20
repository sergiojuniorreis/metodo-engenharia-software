# §17.1 — Arquitetura e desenho de sistema

Carregue ao desenhar sistema novo, mudar estrutura (módulo, fronteira, contrato, persistência) ou
reparar arquitetura. Este setor organiza o **como desenhar**; o **se vale construir** e as quatro
análises ficam no §3, e a **escada de componentes** no §10.

## O desenho em seis passos

1. **Requisito primeiro, em número** (§3): o que o sistema faz, para quem, volume e pico hoje e em
   doze meses, latência, disponibilidade, RPO e RTO, custo por unidade de trabalho.
2. **Fluxo de dados com fronteiras de confiança**: quem fala com quem, por qual contrato, o que
   atravessa cada fronteira. É o mesmo desenho que alimenta a modelagem de ameaça (§17.6).
3. **Menor desenho que atende**: um processo e um armazenamento, até um número medido dizer o
   contrário (§10, escada).
4. **Fronteiras e contratos**: setores nomeados, responsabilidades, o que cada um expõe e consome.
5. **Características de arquitetura viram função de aptidão** (§3): verificação na CI que falha
   quando a característica se perde.
6. **ADR para cada porta de uma via**: escolhido, descartado com motivo, gatilho de revisão.

## Fronteiras

- **Núcleo genérico + domínio plugável** (§2): zero palavra de domínio no núcleo, travado por teste.
- **Dependência aponta para dentro**: regra de negócio não conhece banco, framework, fila nem
  provedor de IA — conhece interfaces. Adaptadores ficam na borda e são trocáveis.
- **Um setor, um dono, uma bateria.** Setor sem dono escrito vira terra de ninguém.
- **Monólito modular é o ponto de partida.** Separar em serviços é decisão de uma via e só se
  paga com motivo medido: times que travam um ao outro, ritmos de deploy diferentes, escala
  muito desigual entre partes.
- **Dependência entre módulos declarada e conferida** por teste de arquitetura (quem pode importar
  quem). Ciclo entre módulos é defeito.

## Contratos e APIs

- **Contrato antes do código**: OpenAPI para HTTP, schema para evento e mensagem. O contrato é a
  fonte; cliente, validação e documentação derivam dele.
- **Erros explícitos e classificados**: transitório, validação, autorização, regra de negócio,
  conflito. O consumidor decide retry pela classe, não pelo texto.
- **Paginação, limite e filtro desde o início** em toda listagem; consulta sem teto é incidente
  agendado.
- **Idempotência em toda escrita exposta** (chave de idempotência aceita e respeitada, §8).
- **Versionamento**: mudança aditiva é compatível; remoção ou mudança de significado é versão maior,
  com expandir → migrar → contrair (§3, reparo).
- **Todo comportamento observável é contrato** (lei de Hyrum, §3): ordem, formato, texto de erro.

## Modelagem de dados

- **O esquema é a decisão mais cara de desfazer.** Nome, tipo, chave e cardinalidade com ADR.
- **Integridade no banco** quando há banco: chave estrangeira, restrição de unicidade, `NOT NULL`
  — a aplicação não é a única guarda.
- **Identificador público não sequencial** (§14.6 item 11); chave interna pode ser outra.
- **Dinheiro em tipo exato** (inteiro em centavos ou decimal), nunca ponto flutuante. Data com fuso
  explícito; armazenamento em UTC, exibição no fuso de quem lê.
- **Migração versionada, reversível e testada** em cópia do volume real antes de produção.
- **Retenção e descarte no desenho** (§11): cada tabela com dado pessoal diz por quanto tempo guarda.
- **Multiempresa**: a coluna de dono (tenant) entra em toda tabela e em todo índice que filtra;
  isolamento testado (§14.6 item 2).

## Comunicação entre partes

| Necessidade | Primeira escolha | Quando subir |
|---|---|---|
| Pedido e resposta, alguém esperando | Chamada síncrona com timeout medido | Espera longa → tarefa assíncrona com consulta de estado |
| Trabalho lento ou em pico | Tabela de estado + worker | Vários consumidores, volume medido → fila gerenciada |
| Avisar outros sistemas de um fato | Outbox + relé (§3D) | Muitos assinantes → barramento de eventos |
| Processo longo com desvio e compensação | Máquina de estados escrita (§8) | Muitos fluxos assim → motor de workflow |

## Revisão de um desenho

Antes de aprovar, o desenho responde por escrito:

- Qual o gargalo esperado e o número que vai mostrá-lo?
- O que acontece quando cada dependência cair (§7, provar o fallback)?
- Onde está o estado, quem pode escrevê-lo e como se resolvem escritas concorrentes (§8)?
- Que componente pode sair sem perder requisito? Se algum pode, sai.
- Como se reverte cada mudança de uma via?
- O que outra pessoa precisa para operar isto sozinha (bus factor, §2)?

## Fontes externas

- Ford, N.; Richards, M.; Sadalage, P.; Dehghani, Z. *Software Architecture: The Hard Parts*.
  O'Reilly, 2021.
- Kleppmann, M. *Designing Data-Intensive Applications*. O'Reilly, 2017.
- Nygard, M. *Documenting Architecture Decisions*, 2011 (cognitect.com/blog) — o formato ADR.
- Martin, R. C. *Clean Architecture*. Prentice Hall, 2017 — a regra da dependência.
- Fowler, M. *MonolithFirst* (martinfowler.com/bliki/MonolithFirst.html).
