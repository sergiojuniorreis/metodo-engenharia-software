# §6 — IA: RAG, veto e custo

Projeto sem IA: "não se aplica — motivo".

- **Fonte primária manda.** Em divergência entre fontes, uma é juiz e isso está escrito no
  projeto. O agente obedece à hierarquia, não "pondera".
- **Recorte por item.** O trecho entregue ao modelo vem do documento **daquele item**.
  Vazamento de trecho — contexto de um item contaminando outro — é defeito caro e silencioso;
  tem teste dedicado.
- **Schema antes da regra.** Esquema mínimo por operação (campos, tipos, valores aceitos),
  validado antes de qualquer lógica. Saída de modelo é entrada não confiável (§11).
- **Citação literal conferida.** Decisão restritiva (recusar, bloquear, reprovar) exige
  confiança alta **e** a citação localizada de volta no texto original. Não achou a citação,
  não houve citação.
- **Resposta inválida:** um retry seguro; depois, conduta conservadora — **seguir e sinalizar
  revisão humana**, nunca descartar em silêncio.
- **O domínio vem da skill**, não do prompt do núcleo: as armadilhas de cada assunto são
  escritas por quem entende do assunto.
- **Escalonamento por custo:** modelo barato primeiro, caro só quando o barato titubeia; cache
  e memória cortam chamada; o gasto por execução é medido na moeda do projeto.
- **Bloco de veto não contradiz a skill.** Cláusula que manda recusar algo que a skill aceita
  produz falso veto — confira executando a skill, não lendo o prompt.
- **Modelo e prompt fixados por versão.** Trocou modelo, provedor ou prompt, roda o corpus de
  regressão (§5, passo 9) antes de subir (§16.2).

# §7 — Ferramentas, MCP e limite de estrago

## Contrato da ferramenta

- **Uma ferramenta = um verbo**, com entradas, saídas e erros explícitos. Ferramenta que faz
  várias coisas conforme o parâmetro vira bug de agente.
- **Idempotência obrigatória** em tudo que escreve.
- **Trava antes do envio**, não correção depois. Barrar antes de gravar é regra; remover
  depois é remendo.
- **Tudo ou nada em lote.** Um item impedido cancela o lote inteiro.
- **Rota oficial sempre que existir**; automação de tela é reserva documentada com o motivo e
  com a permissão descrita abaixo.
- **Nenhuma requisição fora do escopo documentado.** Toda requisição que nós implementamos segue,
  OBRIGATORIAMENTE, um endpoint da documentação que o sistema nos liberou, com o mesmo método e o
  mesmo caminho. Fora dela, nenhuma requisição nossa, seja GET, POST, PUT ou DELETE, nem
  rota interna do app, nem reuso do token da sessão de uma pessoa num fetch nosso. O critério é o
  contrato, não o método HTTP: um GET fora do contrato é tão proibido quanto um POST. O cliente
  que fala com a API confere cada chamada contra o contrato antes de enviar, e um teste prova que
  a rota fora dele é recusada.
- **Onde o contrato não cobre, o agente opera a tela — só com permissão.** Antes, os termos de
  uso do sistema de destino são conferidos e o dono do sistema autoriza por escrito; sem isso,
  não opera. Com a permissão, ele abre a tela e clica como uma pessoa, e só o próprio sistema
  faz as chamadas dele. O agente lê o que a tela recebeu e não pede nada por conta própria.
  Durante a tarefa, uma trava local barra toda escrita (POST, PUT, PATCH, DELETE e GET com verbo
  de escrita), sem liberação por padrão, e registra o que barrou. Estudar uma tela também não
  libera escrita "para ver o que responde". Gravar pela tela só com plano aprovado (simulação →
  OK de uma pessoa → aplicar), com registro e reversão.
- **Nunca logar token, segredo ou payload inteiro** quando um resumo basta.

## Resiliência

- **Timeout por métrica observada**, não por chute, encerrando a espera local mesmo que o
  servidor remoto siga processando.
- **Circuit breaker por integração e por unidade de trabalho** — fechado, aberto, teste de
  recuperação. Ao abrir, usar o caminho seguro e **registrar o desvio**.
- **Retry só em falha transitória confirmada** (timeout, indisponibilidade, conflito de
  revisão), com backoff exponencial e jitter, limite de tentativas e registro de cada uma.
  Nunca em erro de validação, autorização ou regra de negócio. Havendo `Retry-After`, ele manda.
- **Fallback não muda decisão de negócio sem marcar o resultado para revisão humana.**

## Raio de explosão e freio

- **Teto por execução**: quantos registros pode gravar, quanto pode gastar, quanto tempo pode
  rodar. Sem teto, um defeito novo escreve mil vezes antes de alguém acordar.
- **Freio ao alcance do operador**, que para a automação sem depender de nós e sem deixar
  estado pela metade.
- **Sequência de falhas abre o circuito e para com aviso.** Ambiente alterado — layout,
  contrato, resposta inesperada em série — é motivo para parar, não para insistir.
- **Primeira execução em volume reduzido e conferida item a item.** Padrão a ajustar por
  projeto: o menor entre 10% do volume e 20 registros.

## Provar o fallback

Fallback nunca exercitado é fallback imaginário. Em homologação — com dado mascarado ou
fictício, nunca com base real de cliente (§11) — derrube de propósito aquilo de que a solução
depende e exija o comportamento escrito:

| O que derrubar | O que tem de acontecer |
|---|---|
| API do fornecedor fora, ou 500/429 | Circuito abre, trabalho vai para fila ou humano, processo não trava |
| Banco indisponível ou lento | Timeout honrado, operação marcada, nada gravado pela metade |
| Rede cortada no meio do envio | Operação fica `ambigua_requer_verificacao` e é verificada antes de repetir |
| IA fora do schema | Um retry, depois conduta conservadora com sinalização |
| Credencial expirada | Falha classificada e alerta; nunca laço infinito de retry |
| Relógio ou fuso dessincronizado | Data de corte e janela continuam corretas |

Cada linha é um teste com resultado registrado. **Cláusula de resiliência sem teste que a
prove não conta na régua do §4.**

Servidor e cliente MCP, central de agentes e extensões têm regras próprias no §16.
