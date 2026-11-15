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

## MCP — servidor

- Uma ferramenta = um verbo (§7); marque se é só leitura ou destrutiva.
- Servidor remoto com autenticação forte e escopo mínimo (§14.6 itens 11 e 12).
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
