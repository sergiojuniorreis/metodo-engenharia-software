# §17.2 — Desenvolvimento full stack

Carregue ao implementar backend, API, banco, interface ou a ligação entre eles. A implementação
sempre passa pelo portão do §14; este setor diz **como escrever bem cada camada**.

## Conduta de implementação

- **Ler antes de escrever**: a região, quem chama e o que ela chama (§14.1). Nome confirmado por
  busca, nunca suposto.
- **Teste vermelho primeiro**, com o caso real; depois a mudança mínima; depois a suíte inteira.
- **Uma mudança lógica por passo**, com sintaxe e teste a cada passo (§14.2).
- **Sem código morto, sem duplicar o que já existe no projeto, sem dependência nova** fora do §14.3.
- **Função curta com um propósito**, nome que diz o efeito, efeito colateral explícito no nome
  (`gravar…`, `enviar…`).
- **Erro tratado onde se sabe o que fazer com ele**; nos outros pontos, propaga com contexto. Nada
  de `catch` mudo (regra de ouro 6).

## Backend e API

- **Validar na borda, confiar no núcleo**: toda entrada externa passa por schema (tipo, faixa,
  tamanho) antes de chegar à regra (§11).
- **Consulta parametrizada sempre**; nunca concatenação (§14.6 item 10).
- **Transação do tamanho da regra**: nem maior (trava o banco), nem menor (estado partido).
- **Timeout em toda chamada externa**, retry só em falha transitória (§7).
- **Autorização checada por recurso no servidor** (§14.6 item 11); o front esconder o botão não
  é proteção.
- **Configuração por ambiente fora do código**; segredo só no cofre (§14.6 item 7).
- **Log estruturado** com o identificador da execução (§9).

## Banco de dados

- **Índice nasce com a consulta** que precisa dele, conferido pelo plano de execução.
- **N+1 é defeito**: carregue em lote ou por junção; teste que conta as consultas por requisição
  nas rotas críticas.
- **Leitura paginada e com limite**; exportação grande vai para tarefa assíncrona.
- **Migração em passos compatíveis** (expandir → migrar → contrair) para não derrubar a versão
  que ainda está no ar durante o deploy.
- **Regra de conjunto em SQL, não em laço** (§3).

## Interface

A interface web tem módulo próprio: **§16.6** (renderização, orçamento de bundle, componentes,
acessibilidade, segurança no cliente e stack de referência). Aqui ficam só as regras que ligam a
tela ao resto do sistema:

- **Todo estado da tela previsto**: carregando, vazio, erro, parcial, sem permissão, sucesso.
- **Validação no cliente é conforto; a do servidor é a regra** (§16.6.6).
- **Contrato único entre tela e API**: o mesmo schema valida nos dois lados.
- **Ação destrutiva pede confirmação**; ação lenta mostra progresso e não aceita clique duplo.

## Desempenho

Siga a ordem do §10: **medir → dados e API → frontend**, uma melhoria por vez com o número antes
e depois.

| Camada | O que medir | Correções típicas |
|---|---|---|
| Banco | Consultas por requisição, tempo de cada consulta, plano de execução | Índice, junção no lugar de N+1, projeção só das colunas usadas |
| API | Latência p50/p95/p99 por rota, tamanho do payload, chamadas externas por requisição | Lote, paralelo com teto, compressão, paginação, cache de leitura repetida com TTL |
| Rede | Requisições por tela, bytes transferidos | Agrupar chamadas, cache HTTP com validação, CDN para estático |
| Interface | Core Web Vitals no alvo, peso do pacote, cascatas de requisição | Ver §16.6.2 e §16.6.3 |

- **Orçamento de desempenho escrito** (ex.: p95 de uma rota, peso máximo do pacote) e conferido na CI
  quando for característica prometida (função de aptidão, §3).
- **Cache é o último recurso, não o primeiro**: antes dele, a consulta certa.

## Pronto quando

- Teste novo vermelho antes e verde depois; suíte inteira sem vermelho novo (§14.1).
- Toda rota nova com validação de entrada, autorização e teste de recusa.
- Todo estado da interface tratado; nenhuma ação sem retorno ao usuário.
- Ganho de desempenho alegado tem o número antes e depois.


Fontes desta seção: `references/fontes.md`, §17.2.
