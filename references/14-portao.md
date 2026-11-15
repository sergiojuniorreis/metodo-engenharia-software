# §14 — Portão de toda alteração de código

Vale para **qualquer** alteração de código, configuração ou sintaxe — uma vírgula, um regex,
uma chave de JSON, uma skill, o núcleo. O tamanho da mudança regula a **profundidade** da
prova, nunca a **lista**: item que não se aplica se escreve "não se aplica — motivo"; item
omitido conta como falhado. Mudança pequena é onde a auditoria costuma ser pulada e o defeito
entra.

| Momento | O que acontece | Parte |
|---|---|---|
| Antes da primeira edição | Âncora escrita, pauta de segurança respondida, análise do escopo, mapa de impacto, linha de base da suíte, teste vermelho; no reparo, reprodução e teste de caracterização; plano de agentes, se houver | §14.2, §14.6, §3, §14.1, §14.4 |
| Durante | Passo pequeno, hunk conferido contra a âncora, re-ancoragem nos gatilhos | §14.2 |
| Entrou ferramenta nova | Teste do §10, OK do dev, passo a passo executado | §14.3 |
| Antes de entregar | Auditoria do diff, suíte inteira, varreduras, pauta conferida item a item, revisão em cinco eixos (§5), relatório | §14.1, §14.6, §14.5 |

## 14.1 Auditoria total

"Total" são três camadas — **a mudança, o que depende dela e o que ela usa** — conferidas em
dois momentos.

### Antes de editar: o mapa de impacto

- **Ler o código real** da região tocada, de quem a chama e do que ela chama. Nunca editar de
  memória — nem da memória desta conversa: depois de resumo de contexto, retomada ou retorno
  de agente, o arquivo se relê.
- **Achar todo uso** do que vai mudar — símbolo, chave, rota, campo, mensagem, flag — no
  repositório inteiro: código, teste, documentação, configuração, build. Arquivo grande que a
  busca trata como binário se busca em modo texto (ex.: `grep -a`).
- **Achar as cópias:** fonte × gerado ou compilado, trecho que outro componente recorta por
  nome, versão arquivada, espelho em outra pasta ou máquina. A mudança vai à fonte; a cópia se
  regenera e um teste prova a igualdade.
- **Saber de onde o teste lê.** Teste que carrega a versão instalada, e não a do repositório,
  dá verde falso.
- **Conferir o terreno:** arquivo limpo no git, ninguém mais editando (hash antes de gravar),
  versão de cada peça, fim de linha e codificação de cada arquivo a tocar.
- **Rodar a suíte antes — a linha de base.** Falha que já existia é registrada como
  pré-existente: nem escondida, nem atribuída à mudança.
- **Escrever o teste que falha sem o conserto** e vê-lo falhar.

### Depois de editar: a auditoria do diff

- **Arquivos alterados** (`git diff --stat`) iguais aos previstos no Escopo. Arquivo a mais —
  formatador, conversão de fim de linha, ferramenta que reescreve fonte — é investigado, não
  ignorado.
- **Diff lido inteiro, hunk a hunk**, cada um ligado a um item da âncora (§14.2).
- **Sintaxe de todo arquivo tocado** conferida pela ferramenta da linguagem (ex.:
  `node --check`, `py_compile`, parser de JSON/YAML, linter) — nunca no olho.
- **Suíte inteira**, não só o teste novo, comparada à linha de base pelo código de saída:
  nenhum verde virou vermelho; o teste novo era vermelho e agora é verde.
- **Todo chamador do mapa** continua compatível; contrato público quebrado é versão maior (§5).
- **Varreduras:** segredo, dado pessoal, número nosso em campo que terceiro lê (§12),
  depuração esquecida, `catch` mudo, comentário com histórico.
- **Fim de linha e codificação** iguais aos de antes; cópias regeneradas e iguais à fonte;
  README, versão e documentação no mesmo commit.
- **Releitura fria** do diff como revisor que não o escreveu, caçando a borda: vazio, nulo,
  um item só, unidade, acento, número no formato local (separador decimal e de milhar), fuso,
  repetição, concorrência.

## 14.2 Contra o drift

Drift é a lógica se afastar do objetivo **sem que ninguém tenha decidido**: escopo que cresce,
premissa que muda em silêncio, nome de função suposto, conserto que vira refatoração, código
que diverge do teste, da documentação ou da cópia. Sessão longa piora tudo: depois de um resumo
de contexto, a lembrança do arquivo é velha.

**A âncora**, escrita para o dev antes da primeira edição:

| Campo | Conteúdo |
|---|---|
| Objetivo | Uma frase verificável |
| Aceite | O comando ou teste que prova, com o resultado esperado |
| Escopo | O setor e os arquivos que podem mudar |
| Invariantes | O que não pode mudar: contrato, formato de saída, comportamento dos outros casos |
| Fora | O que vi e não vou mexer |

Tarefa que atravessa sessões ou resumo de contexto guarda a âncora em arquivo e a relê na
retomada — o arquivo sobrevive ao resumo; a conversa, não.

### Durante a edição

- **Um passo, uma mudança lógica**, seguida de sintaxe e teste. Nunca dez edições e um teste
  no fim.
- **Todo hunk responde "a que item da âncora eu sirvo?"** Sem resposta, sai do diff.
- **Defeito achado no caminho vai para o Fora**, com arquivo:linha e evidência; o dono decide.
  "Já que estou aqui" é drift.
- **Nome, função, rota, campo e flag confirmados por busca** antes de usar. Suposto não entra.
- **Tentativa que falhou é revertida** antes da próxima. Remendo sobre remendo é drift
  acumulado.
- **Duas tentativas do mesmo conserto falharam: para de editar** e volta ao diagnóstico —
  reproduzir, isolar, ler o estado real. Terceira tentativa às cegas é proibida.

### Re-ancoragem obrigatória — reler a âncora e o diff atual

- a cada teste vermelho inesperado;
- depois de resumo de contexto ou retomada de sessão;
- ao receber resultado de agente;
- antes de tocar arquivo fora do Escopo;
- antes de entregar.

**Mudança de rumo é declarada.** A evidência contradisse a premissa: para, diz o que mudou e
por quê, reescreve a âncora e, se o escopo cresceu, pede o OK do dono. Objetivo não se troca no
meio do código.

**Uma fonte de verdade.** Regra que existe em dois lugares diverge; consolida-se ou trava-se a
igualdade por teste.

## 14.3 Ferramenta nova: o passo a passo do dev

Conta como ferramenta nova: dependência ou biblioteca, CLI, runtime, extensão, serviço ou API
externa, servidor MCP, hook, tarefa agendada, variável de ambiente, arquivo de configuração ou
de credencial, porta de rede, permissão de sistema, escopo OAuth novo — e a troca de versão
maior de uma que já existe.

**Ordem:** teste de necessidade do §10, por escrito, com a alternativa mais simples e por que
ela não serve → **OK do dev antes de instalar** → versão exata travada, licença e origem
conferidas → **passo a passo executado e entregue**.

O passo a passo segue este formato, sem pular bloco:

```text
## <Ferramenta> <versão exata> — configuração
Para que serve aqui · Por que não a alternativa · Onde roda · Quem opera · Custo e licença

Pré-requisitos   o que precisa existir, cada um com o comando que confere
Instalar         comandos exatos, numerados, cada um com a saída esperada
Configurar       arquivo e caminho exatos, variável e valor (segredo: onde fica, nunca o valor)
Conferir         o comando que prova que funciona e a saída esperada
Outra máquina    o que se repete em cada máquina e o que já vem pelo repositório
Quando falhar    sintoma → causa provável → o que fazer
Desfazer         comandos de remoção e como confirmar que voltou ao estado anterior
```

- **Cada comando foi executado** no ambiente real, com a saída conferida. O que não foi
  executado vem marcado **NÃO EXECUTADO — motivo**.
- **No shell e no sistema declarados no projeto** (ou no `PERFIL.md`); sem declaração,
  pergunte antes. Comando de um shell colado em outro (Bash no PowerShell, por exemplo) é passo
  quebrado.
- **Exato ou não é passo:** caminho, nome de variável, versão. "Configure as credenciais" não
  é passo.
- **O passo a passo vai para o repositório** (README ou documento de configuração) no mesmo
  commit, além de ir na mensagem. Chat se perde; bus factor 1 é defeito.

## 14.4 Agentes com orçamento

Vale para agentes usados **no trabalho de desenvolvimento**. Agentes que são o **produto**
(central de agentes, orquestração) seguem o §16.2.

Subagente não é velocidade de graça: cada um relê contexto do zero e o fan-out multiplica a
conta.

**O padrão é zero agente.** Faz-se direto o que cabe no contexto (dois ou três arquivos, um
log recortado), o que é sequencial, o que depende do que acabou de ser visto e a busca de um
símbolo conhecido.

**Agente entra por um destes motivos, e o motivo é dito:**

| Motivo | Exemplo |
|---|---|
| Frentes independentes de escopo fechado, que ganham com o paralelo | Sistemas externos diferentes; famílias de skill diferentes |
| Varredura que despejaria arquivos no contexto principal — fica só a conclusão | Achar todos os usos num acervo grande |
| Olho independente, sem o viés de quem escreveu | Revisão adversarial; crítico dos números |

**Antes de lançar, o plano é dito ao dev** — informa, não pede licença, e o dev pode parar:
quantos agentes, o que cada um faz, por que não se faz direto, o modelo de cada um (busca e
extração no mais barato que dá conta, julgamento no mais forte), a entrada já recortada
(caminhos, trechos, arquivo:linha — nunca "leia o repositório"), a saída com formato e tamanho
fixos (conclusão + evidência, sem despejo) e a estimativa de tokens apoiada numa execução
medida parecida — sem base, "não medi".

**Quantos: os necessários, nem um a mais.** Não existe número fixo; o número sai das frentes
da tarefa, contadas no plano.

- **Uma frente independente, um agente** — e só a frente que não cabe no contexto principal.
  Frentes que leem a mesma entrada ou dependem uma da outra viram um agente só, ou uma
  sequência.
- **Cada agente se justifica no plano:** a frente dele, por que não se junta a outra, por que
  não se faz direto. Agente sem frente própria não sai.
- **Sinais de exagero**, que derrubam o plano antes de lançar: agente para o que cabe em dois
  ou três arquivos; dois agentes lendo a mesma entrada; mais de um crítico para a mesma
  conclusão; agente sem formato de saída fixo; estimativa na casa do milhão de tokens sem um
  motivo escrito que a justifique.
- **Workflow de orquestração no desenvolvimento**, só a pedido explícito do dev.

### Porte e freio

- **Lote grande começa por um piloto**; o resto só sai se o piloto provar formato e caminho
  (como a primeira execução em volume reduzido, §7).
- **Itens em lote por agente**, nunca um agente por item.
- **Agentes que escrevem** recebem arquivos disjuntos ou cópia isolada (ex.: git worktree);
  dois agentes no mesmo arquivo é escrita concorrente sem revisão (§8). A junção é feita no
  contexto principal, com a auditoria do §14.1.
- **Delegou, não refaz:** a mesma busca não roda também no contexto principal. Agente cujo
  contexto ainda serve é continuado, não recriado.
- **Primeiro resultado mostrou abordagem errada:** os demais param na hora.

### Depois

- **Saída de agente é afirmação, não evidência.** As citações que sustentam decisão são
  conferidas no arquivo antes de agir.
- **Prestação de contas:** agentes usados, modelo, tokens e tempo de cada um, e se o resultado
  mudou a decisão. Agente que não acrescentou nada vira lição de dimensionamento na memória.

## 14.5 O relatório da entrega

Toda entrega de código termina com este bloco. Campo vazio não existe: tem evidência, ou
"não se aplica — motivo", ou "NÃO FEITO — motivo".

```text
Âncora        objetivo — atendido / parcial / não
Aceite        comando → resultado · vermelho antes: evidência
Invariantes   cada um → o teste que o protege
Auditoria     arquivos (lista) · chamadores conferidos · cópias · sintaxe → ferramenta e
              resultado · suíte antes × depois · varreduras · fim de linha
Revisão       cinco eixos (§5) · Crítico/Importante pendentes: 0
Drift         hunks fora da âncora · mudanças de rumo · Fora (vi e não mexi)
Ferramenta    nenhuma / nome e versão + onde está o passo a passo
Agentes       0 / quantos, modelo, tokens, o que mudaram
Segurança     pauta do §14.6, item a item → teste e resultado, ou não se aplica — motivo
Análise       as quatro do §3 → decisão de cada uma, ou não se aplica — motivo; no reparo,
              reprodução, cerca de Chesterton e teste de caracterização
Módulo §16    qual se aplica → itens conferidos, ou não se aplica — motivo
Reverter      comando ou commit
```

## 14.6 Pauta de segurança

Todo projeto novo e toda alteração de código começam por esta pauta. Cada item é uma pergunta
de segurança que a mudança responde por escrito, com a evidência que vai entregar.

### Como se usa

- **Projeto novo:** é a 8ª pergunta do estudo de abordagem (§3); cada item que se aplica vira
  requisito do desenho, com o teste previsto.
- **Alteração de código:** respondida por escrito junto da âncora (§14.2), item a item — "se
  aplica → a evidência que vou entregar" ou "não se aplica — motivo". Item omitido conta como
  falhado; o tamanho da mudança regula a profundidade da resposta, nunca a lista.
- **Entrega:** cada item que se aplica aparece na linha Segurança do relatório (§14.5) com o
  teste e o resultado. Item que se aplica e não tem teste é falha aberta: regra sem teste é
  boato.
- **Auditoria nova:** todo achado confirmado vira item novo desta pauta, escrito como regra
  geral. A pauta só encolhe por decisão do dono.

### A pauta

1. **Falha fechada.** O que a mudança guarda, lembra, registra ou devolve — memória, log,
   relatório, instrução ao modelo — entra por lista explícita do que pode entrar. Item sem a
   declaração entra vazio, nunca inteiro.
   *Evidência:* teste que reprova todo item do catálogo sem a declaração (lista vazia vale).
2. **Isolamento por dono.** Dado de um agente, cliente, empresa, tenant ou usuário volta só para
   quem o criou. Agregação e consulta filtram por quem chama, não só pelo nome da operação
   liberada.
   *Evidência:* teste em que A grava, B consulta e B não vê nada de A — nem argumento, nem
   exemplo de erro.
3. **Tudo o que chega ao modelo é envio.** Instrução de abertura, memória injetada, exemplo de
   erro e argumento lembrado saem da nossa fronteira como qualquer chamada (§11). A ofuscação
   cobre todos os tipos de dado pessoal do §11 e o número nosso do §12.
   *Evidência:* um teste por tipo — nome, documento nacional (ex.: CPF), telefone, endereço,
   e-mail, conta bancária, documento, custo e margem — mostrando o valor mascarado no que vai
   ao modelo.
4. **Proteção por classe, não por ferramenta.** Operação que faz o mesmo que uma protegida
   herda a proteção. O mapa de impacto (§14.1) procura as equivalentes pelo efeito — enviar
   e-mail, gravar, aprovar —, não pelo nome.
   *Evidência:* teste que confere a mesma proteção em todas as equivalentes.
5. **Aceite humano conferido pelo servidor.** Operação que envia, grava ou aprova em nome de uma
   pessoa exige uma prova que o modelo não consegue produzir: código de uso único mostrado fora
   do modelo, ou aprovação no painel com a sessão da pessoa. Texto devolvido ao modelo ("só
   depois que ele disser manda") e pergunta de permissão do cliente não são trava. Sessão em
   que o modelo lê conteúdo de terceiro e tem ferramenta que escreve se trata como sessão sob
   injeção (§11).
   *Evidência:* teste em que a chamada sem a confirmação é recusada e nada sai; a mesma
   confirmação repetida é recusada; teto diário com aviso.
6. **A mesma régua em todos os modos.** Local, teste, homologação e produção aplicam a mesma
   validação de segurança. O modo pode escolher o valor padrão de um campo vazio; nunca
   afrouxar a checagem de um campo preenchido.
   *Evidência:* teste da partida em cada modo com o valor fraco, reprovado em todos.
7. **Segredo só no cofre.** Arquivo de configuração, comando gerado para colar, histórico do
   shell e arquivo de configuração de cliente de IA ou de ferramenta (ex.: o arquivo de
   configuração do cliente MCP) não guardam segredo em texto claro. O segredo vem do cofre do
   sistema ou do gerenciador de segredos do ambiente (ex.: DPAPI, Keychain, libsecret, Vault,
   secret manager da nuvem; quando a aplicação cifra por conta própria, AES-256-GCM); o
   exemplo de configuração não tem nenhum.
   *Evidência:* varredura do exemplo de configuração sem segredo; teste em que a partida recusa
   quando o cofre não tem a chave.
8. **O artefato leva só o que deve.** Deploy, pacote, zip, imagem e extensão publicada têm a
   lista do que sobe conferida pela própria ferramenta antes de publicar. Relatório de
   auditoria, dado de teste e script interno ficam fora.
   *Evidência:* a listagem do upload gerada pela ferramenta de deploy do projeto, anexada à
   entrega (ex.: no Cloud Run, `gcloud meta list-files-for-upload`).
9. **Histórico também é código.** A varredura de segredo cobre o histórico inteiro do
   repositório — cuja raiz se confere antes, com `git rev-parse --show-toplevel` — e procura
   pelo formato da chave, não por pedaço da chave vazada. Chave achada é revogada no provedor
   antes de qualquer evolução (§12); reescrever o histórico não substitui a revogação.
   *Evidência:* saída da varredura do histórico; revogação conferida pelo dono no console do
   provedor.
10. **Segurança clássica de aplicação** (web, mobile, desktop, ERP web). Entrada validada no
    servidor; queries parametrizadas; saída escapada por contexto (XSS); proteção CSRF em
    sessão por cookie; destino de URL em lista permitida (SSRF); upload com tipo real, tamanho
    máximo e fora da raiz pública; CORS restrito; cabeçalhos de segurança; debug desligado em
    produção.
    *Evidência:* teste por categoria aplicável ou saída de análise estática (SAST) sem achado
    crítico.
11. **Autenticação e autorização.** Autenticação por biblioteca ou provedor consolidado, nunca
    caseira; senha com hash lento (Argon2id ou bcrypt); MFA em conta administrativa; token com
    expiração curta e revogável; autorização checada no servidor em cada recurso (IDOR); ID
    público não sequencial.
    *Evidência:* teste em que um usuário sem permissão é recusado em cada rota protegida.
12. **Escopo mínimo em integração OAuth** (Microsoft, Google, ERP, marketplace). Permissão
    delegada antes de permissão de aplicação; cada escopo justificado; token guardado no cofre
    (item 7); separação por tenant ou empresa (item 2).
    *Evidência:* lista de escopos pedidos × usados; teste com escopo ausente falhando fechado.
13. **Servidor MCP e ferramenta de agente** (§16.2). Definição das ferramentas fixada por versão
    ou hash; nenhum token do usuário repassado a terceiro; servidor local só em localhost, com
    validação de Origin.
    *Evidência:* teste de definição de ferramenta alterada sendo recusada; teste de Origin
    inválida recusada.
14. **Extensão e agente no navegador** (§16.4). Permissões e hosts mínimos; mensagem entre
    contextos com remetente validado; conteúdo de página tratado como dado, nunca comando.
    *Evidência:* manifesto auditado; teste de mensagem de origem desconhecida recusada.
15. **Cadeia de suprimentos.** Lockfile versionado; auditoria de dependências automática na CI;
    extensão, servidor MCP ou pacote de terceiro revisado antes de instalar (§14.3).
    *Evidência:* saída da auditoria no commit atual.
