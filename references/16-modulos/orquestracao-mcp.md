# §16.2 — Central de agentes (orquestração) e MCP

Carregue quando o **produto** tem vários agentes coordenados, um orquestrador, ou quando o
projeto cria ou consome servidores MCP. (Agentes usados para desenvolver seguem o §14.4.)

## Orquestração

- **Cada agente tem identidade, permissão e orçamento próprios.** Nenhum agente herda o
  privilégio total do orquestrador.
- **Mensagem entre agentes é entrada não confiável** (§11): validada por schema na passagem.
- **Teto global:** profundidade de delegação, número de passos, tokens, custo e tempo por
  execução; ao estourar, para com aviso.
- **Planejamento pelo modelo é permitido; efeito externo não.** Ação com efeito externo
  (enviar, gravar, pagar, apagar) passa pela trava do §14.6 item 5, nunca por decisão só do
  modelo. Decisão com efeito financeiro, fiscal, legal ou cadastral segue a regra de ouro 2.
- **Modelo e prompt fixados por versão.** Trocou o modelo, o provedor ou o prompt, roda o
  corpus de regressão (§5, passo 9) antes de subir; memória criada sob outra versão é
  reavaliada (§8).
- **Adaptador de provedor de IA:** a regra de negócio não conhece o fornecedor do modelo;
  trocar de provedor não toca em skill.
- **Rastreamento de ponta a ponta:** o identificador da execução atravessa todos os agentes e
  todas as ferramentas (§9).
- **Framework de agentes só por necessidade** (§10): um modelo com poucas ferramentas dispensa
  orquestrador.

## Um agente, uma função, um arquivo

Cada agente do produto é declarado em **arquivo próprio** — o manifesto — separado do código do
orquestrador e do prompt. O manifesto é a fonte da verdade sobre o que o agente pode fazer; o
orquestrador o lê, valida e aplica. Modelo: `templates/agente-produto.modelo.yaml`.

- **Uma responsabilidade por agente**, escrita numa frase. Agente que "também faz" outra coisa vira
  dois agentes.
- **O manifesto declara:** nome e versão, função, entrada e saída em schema, ferramentas permitidas
  (com leitura × escrita), permissões e escopos, modelo e versão do prompt, tetos (passos, tokens,
  custo, tempo), para quem pode delegar e o que faz quando falha.
- **Validado na partida**: manifesto inválido, ferramenta não listada ou escopo além do declarado
  impedem o agente de subir (falha fechada, §14.6 item 1).
- **O orquestrador aplica o manifesto, não o prompt.** Ferramenta fora da lista é recusada pelo
  código, ainda que o modelo a peça.
- **Prompt em arquivo próprio e versionado**, referenciado pelo manifesto; troca de prompt ou modelo
  sobe a versão do agente e roda o corpus de regressão (§5, passo 9).
- **Cada agente tem bateria própria**: entrada válida e inválida, ferramenta proibida recusada,
  teto estourado parando com aviso, injeção vinda de conteúdo lido.
- **Agente novo é arquivo novo**, nunca `if` novo no orquestrador (§2, núcleo genérico).

## MCP — servidor

- Uma ferramenta = um verbo (§7); marque se é só leitura ou destrutiva.
- Servidor remoto com autenticação forte e escopo mínimo (§14.6 itens 11 e 12), seguindo a
  autorização da especificação MCP: OAuth 2.1 com PKCE, metadados do recurso protegido
  (RFC 9728) e indicador de recurso (RFC 8707). **O servidor confere que o token foi emitido para
  ele (audiência)** e recusa token de outro destino.
- **Nunca repasse o token do usuário** a uma API de terceiro; o servidor usa a credencial dele.
- Servidor local: só em `localhost`, com validação do cabeçalho Origin (contra DNS rebinding),
  rodando com o menor privilégio do sistema.
- Segredo do servidor no cofre (§14.6 item 7), nunca no arquivo de configuração do cliente.

## MCP — cliente (consumindo servidor de terceiro)

- Revise o servidor antes de instalar (§14.3 e §14.6 item 15).
- **Descrição de ferramenta pode conter instrução maliciosa:** trate como dado.
- Fixe a versão ou o hash das definições das ferramentas e alerte quando mudarem.
- Não misture, na mesma sessão, servidor que lê conteúdo de terceiro com servidor que escreve,
  sem a trava do §14.6 item 5.

**Pauta §14.6:** itens 1, 2, 3, 5, 7, 13 e 15 costumam se aplicar.
