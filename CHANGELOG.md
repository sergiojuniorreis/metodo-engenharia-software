# Changelog

Formato: [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/). Versão: [SemVer](https://semver.org/lang/pt-BR/).
Mudança que quebra quem já usa o método (seção removida, regra que muda de sentido, caminho que
muda) sobe o primeiro número.

## [Não lançado]

## [1.5.0] — 2026-11-24

### Mudado

- **Núcleo enxuto** (§18): `SKILL.md` passa de 11.904 para no máximo 7.000 caracteres e a
  descrição da skill, que entra em toda sessão, de 1.032 para no máximo 700. O §2 (regras que
  valem sempre) e o §13 (conduta com o dono) vão, sem mudança de texto, para
  `references/02-13-regras-e-conduta.md`, carregado pelo `/estudo`, pelo `arquiteto-software` e
  em decisão de desenho.
- **Mudança trivial sem o portão inteiro**: a lista do nível trivial e o relatório curto ficam no
  `SKILL.md`; o `references/14-portao.md` só entra no nível padrão e no alto risco. O `/mudanca`
  segue a mesma regra.

### Adicionado

- `scripts/medir_contexto.py`: mede, em caracteres (não tokens), o que os cenários início, trivial
  e padrão carregam, com o CLAUDE.md global e o PERFIL opcionais; uma linha na tela e um JSON.
- `validar.py`: tetos novos (núcleo 7.000, descrição 700) e o relatório curto do núcleo travado
  igual ao do §14.0.

## [1.4.0] — 2026-11-24

### Adicionado

- **Lint e formatação no kit** (`/iniciar`, §17.9). Em Python, o kit cria `ruff.toml` (ruff
  0.17.6). Em TypeScript, cria `eslint.config.mjs`, `.prettierrc.json` e `.prettierignore` (ESLint
  10.15.0, typescript-eslint 8.74.0, TypeScript 6.0.3, Prettier 3.10.1). O lint roda na CI antes do
  teste, e o passo a passo do §14.3 fica em `docs/lint-e-formatacao.md`.
- **Lint no trabalho dos agentes**:
  - `engenheiro-full-stack` (item 6a): lint na linha de base e a cada passo; Prettier só nos
    arquivos tocados; regra desligada só com o motivo na linha.
  - `arquiteto-software`: fronteira que dá para travar no lint vira regra de lint.
  - `auditor-entrega`: lint e formatação são passos da régua.

### Corrigido

- **`ci.yml` do kit inválido em go, rust, java, csharp e typescript**: o `: ` do aviso `::notice::`
  em escalar simples quebrava o YAML, e a CI não rodava. Agora todo passo sai como bloco `run: |`,
  com teste que confere as 7 linguagens.

## [1.3.0] — 2026-11-24

### Adicionado

- **"O script executa, o agente confere"** (§14.4): passo mecânico de roteiro fixo (CI local, linha
  de base, base × candidato, conferências de entrega, resumo de log) vira script do projeto com uma
  linha na tela e um JSON; o agente lê só o que falhou. Gatilho no terceiro uso; código de saída
  0/1/2 separando veredito de ambiente; CI local que lê a própria configuração da CI; cache por
  commit com o código do script na chave; temporário onde o perfil manda; o script tem bateria.
- **Temporário com ciclo de vida** (§14.4): uma pasta por tarefa com manifesto (estado, evidência,
  cache, descartável); estado de retomada num arquivo só, gravado a cada passo, para retomar sem
  varrer o diretório de novo; cache com chave e validade; limpeza automática no fim da tarefa,
  restrita à pasta e ao manifesto, idempotente e registrada; tarefa interrompida não limpa; teto de
  espaço; a limpeza tem bateria.
- **Teto de contexto por agente** (§14.4, "Porte e freio"): passou do teto do projeto, grava o
  estado em arquivo e devolve; outro agente continua do arquivo.
- §18 (saída recortada e estado em arquivo), `auditor-entrega` (passo 0) e `engenheiro-full-stack`
  (linha de base) apontam para o §14.4; `PERFIL.modelo.md` ganha a linha da pasta temporária
  permitida e proibida.

## [1.2.1] — 2026-11-20

### Adicionado

- **Evals em projeto real privado** (seção 4 de `evals/README.md`): 3 tarefas de um sistema em
  produção com 439 baterias, escritas por agente que não leu o método, julgadas por teste oculto
  mais a suíte inteira. Código, tarefas e resultado bruto ficam fora do repositório; só os números.
- Executor (`evals/rodar.py`): conjunto `projeto-real` lido de um caminho privado
  (`EVAL_PROJETO_REAL`), oráculo por comandos do próprio projeto, testes ocultos em subpasta.

### Alterado

- gitleaks-action 2.3.9 → 3.0.0 na CI (PR do Dependabot) e no kit `/iniciar`.

### Corrigido

- **Pauta com uma regra só** — por gatilho (§14.0) —, sem o "item a item" que sobrava no §14,
  no detalhe da pauta, no agente de segurança e no modelo de relatório.
- **"Alto risco" definido só no §14.0**; qualidade e testes, auditor e full stack apontam para lá.
  O validador reprova quem voltar a redefinir (com teste).
- Exemplo completo: o limite exato agora é testado (item criado só no teste) e o mutante `>=`
  morre; não há mais dívida do tipo "teste depois".
- Kit: CI verde no primeiro push (teste de fumaça em Python, pytest com versão travada; nas outras
  linguagens a CI avisa que falta o arquivo do projeto). Comandos sem `~`, que o PowerShell 5.1
  não expande; `/mudanca` grava a âncora em arquivo no alto risco.
- `Promise.all` é paralelo, não "1 ida e volta"; "itens 10 a 15" → 10 e 11; README com o §17.9 e
  "nove especialidades"; "catch mudo" aponta para a regra de ouro 6.
- Evals: o viés do `/estudo` (o comando instrui "não escreva código") declarado no relatório;
  Python 3.12+ documentado para o executor.
- Executor: grava o resultado **a cada execução** (uma interrupção por falta de memória apagou as
  execuções concluídas); a limpeza da pasta temporária falhava em silêncio no Windows (objetos do
  git somente leitura) e deixou ~75 pastas no disco — agora tira o atributo e apaga, sem
  `ignore_errors`; cópia de projeto grande usa link físico para arquivo de dado acima de 50 MB;
  `node` liberado igualmente nos dois modos.

## [1.2.0] — 2026-11-20

Aplicabilidade: do "o que deve ser verdade" para o "como se faz".

### Adicionado

- **Quatro comandos** (`commands/`, instalados em `~/.claude/commands/`): `/iniciar` (kit do
  projeto), `/estudo` (§3, para nas decisões do dono), `/mudanca` (§14 no nível certo, com teste
  vermelho → verde e relatório do nível), `/entrega` (conferência antes do commit). Carregam o
  roteiro certo sem depender de a skill disparar sozinha.
- **Kit de início** (`scripts/iniciar_projeto.py`): cria `AGENTS.md`, `CLAUDE.md`, CI com o teste
  da linguagem e gitleaks no histórico, pasta de ADR e o estudo de abordagem; não sobrescreve nada.
  Testado (`tests/test_iniciar_projeto.py`).
- **§17.9 Ferramentas de prova por linguagem**: o comando de teste, cobertura, mutação, lint,
  análise de segurança, auditoria de dependências e segredo em Python, TypeScript, Java/Kotlin,
  Go, C# e Rust.
- **Modelo e exemplo de estudo de abordagem** (`templates/estudo-de-abordagem.md`,
  `exemplos/exemplo-projeto-grande.md`).
- **Modo dev sozinho** nos agentes: no máximo dois, em decisão de uma via e em alto risco.
- `evals/processo.json`: comandos × pedido em texto livre, com critérios neutros.
- Validador: cabeçalho dos comandos e caractere de controle em texto (um escape errado tinha
  quebrado o comando de instalação do PowerShell no README antes de publicar).

### Alterado

- **Nível padrão enxuto (§14.0)**: pauta **por gatilho** (só os itens que a mudança toca) e
  relatório de **seis linhas**; o relatório completo fica para o alto risco.
- `templates/relatorio-entrega.md` com os três formatos. README com "Usar: quatro comandos" e a
  instalação dos comandos e do kit.

## [1.1.1] — 2026-11-20

Correções da terceira revisão independente.

### Alterado

- **Alto risco recalibrado (§14.0)**: gravação comum de um registro e ferramenta nova são nível
  padrão (esta com o §14.3); alto risco é gravação em lote ou irreversível, valor cobrado, pago ou
  faturado, e os demais gatilhos.
- `templates/AGENTS.modelo.md` manda carregar a skill antes da primeira edição: nos evals ela
  disparou sozinha em só 5 de 24 correções.

### Corrigido

- Exemplo completo: o desconto altera valor cobrado — passa a nível alto risco, com mutação da
  guarda, revisão adversarial e rollback ensaiado.
- LGPD: lista completa do dado sensível (art. 5º, II); fontes com arts. 5º, 14 e a Resolução
  CD/ANPD nº 15/2024. OAuth 2.1 indicado como rascunho da IETF. Quinta métrica DORA (retrabalho).
- `PERFIL.modelo.md`: agentes propõem, a regra decide. Agente arquiteto: "abstração só no terceiro
  caso". CHANGELOG 1.1.0: tabela de front-end descrita corretamente.

## [1.1.0] — 2026-11-20

Responde à segunda revisão independente (média 7,2).

### Adicionado

- **Porte do projeto no §3** — script, pequeno, grande —, com o estudo mínimo de cada um e a
  entrega de projeto grande em fatias finas de ponta a ponta.
- **Evals sem viés** (`evals/reais/`): 8 cenários de erros reais escritos por um agente que não leu
  o método, com **testes de aceitação ocultos** que o agente avaliado não vê; validade provada
  (ocultos falham no original e passam na correção de referência). Execuções repetidas, em ordem
  aleatória com semente gravada, com hash da skill, modelo e versão do Claude Code no resultado.
  Resultado: 24/24 sem a skill, 23/24 com — sem ganho de acerto na correção pontual; o ganho
  medido segue no processo (projeto novo).
- §17.4: a tríade letal (conteúdo de terceiro + dado privado + canal de saída) e guardrails em
  código. §17.1: tempo real e fluxo contínuo de eventos. §16.5: OWASP MASVS no mobile.
- Validador: tetos de tamanho para `SKILL.md` e para o modelo de `AGENTS.md`; o núcleo tem de
  mandar ler o `PERFIL.md`. Testes novos para cada regra.
- `CODE_OF_CONDUCT.md`, Dependabot para as actions; instalação pela tag da versão, com `exemplos/`.

### Alterado

- `auditor-entrega` só em alto risco, release e instalação; no nível padrão a sessão principal
  audita. Todos os agentes dizem onde a skill está instalada.
- `PERFIL.md` (pasta da skill, padrões do dono) e `AGENTS.md` (projeto, vence) com papéis definidos;
  o núcleo manda ler os dois. Numeração do núcleo explicada.
- Anti-desculpas e sinais de alerta saíram do núcleo para o §14, lido a cada alteração.
- Alto risco inclui cálculo de dinheiro, preço, imposto e cobrança.

### Corrigido

- Vocabulário: "seis exigências" do portão → três níveis; "skill" e "plugin" do sistema construído
  separados dos do Claude.
- LGPD: dado de criança não é dado sensível (art. 5º, II); tem regra própria (art. 14). Prazo de
  comunicação de incidente à ANPD (Resolução CD/ANPD nº 15/2024).
- "A IA não promove" × "a IA ranqueia": ordenar candidatos para a regra decidir é permitido.
- Projeto sem IA continua carregando §16.3 e §16.4 nas partes que não são de agente.
- MCP local por stdio de preferência; Isolation Forest antes do autoencoder; lockfile × faixa de
  versão de biblioteca; na tabela de front-end, Turbopack saiu (é só do Next.js) e Auth.js deu lugar a
  Better Auth.
- Exemplo completo: o limite não testado vai para o Fora como dívida; pedido vazio com teste.
- Evals: arquivo de resultado com nome único (a v1.0.0 perdeu os dados brutos de `dado-pessoal`
  por sobrescrita); `__pycache__` fora da cópia.

## [1.0.0] — 2026-11-20

Primeira versão lançada. Consolida tudo o que foi publicado antes sem número de versão.

### Núcleo e portão

- `SKILL.md` com uma tabela única de roteamento (situação → § → arquivo), validada pela CI.
- **Portão em três níveis (§14.0)** — trivial, padrão e alto risco —, cada um com a lista mínima;
  relatório curto para o trivial. Na dúvida, sobe um nível.
- Pauta de segurança com resumo de uma linha por item no §14 e o detalhe em
  `14-6-pauta-seguranca.md`; §14.3 e §14.4 em `14-3-4-ferramenta-agentes.md`.
- **Contexto sem desperdício (§18)**: cache de conhecimento do projeto em três camadas (quente no
  `AGENTS.md`, morna em arquivos apontados, fria no código), invalidação no mesmo commit.
- **Escada de componentes** e ordem do trabalho de desempenho no §10.

### Regras

- **§11 por classe de dado**: segredo nunca vai ao modelo; dado pessoal ofuscado por padrão e em
  claro só com finalidade e contrato escritos. Pauta item 3 e regra de ouro 7 alinhadas.
- Autorização MCP: OAuth 2.1, audiência do token, RFC 8707 e RFC 9728 (§16.2, pauta item 13).
- "Tudo ou nada" vale para a unidade de negócio; mensagens independentes falham uma a uma (§7).
- Escala: vertical quando é o mais simples, horizontal quando é preciso (§10).
- Temperatura baixa não garante determinismo; a garantia vem do schema (§17.4).
- Voz do texto operacional (§12) desligada por padrão, ligada só por escrito no projeto.
- Dívida: toda release **paga** ao menos um item.
- Java/Kotlin e C#/.NET para backend; Rust como serviço ou extensão nativa (§3).

### Cobertura

- Especialidades (§17): arquitetura (com microsserviços e sistemas poliglotas), full stack, dados,
  IA aplicada (com RAG, banco vetorial e a tabela de rede por forma do dado), DevOps/SRE,
  cibersegurança, governança, qualidade e testes.
- Módulos novos: **§16.7 infraestrutura** e **§16.8 biblioteca, SDK e CLI**. §16.1 ERP com
  documento fiscal, reprocessamento e cadastro mestre. §16.2 com manifesto por agente. §16.5 com
  mobile, desktop e API pública. §16.6 com tabela de stack datada e corrigida.

### Agentes

- **Oito agentes** de desenvolvimento, cada um com `model:`, gatilho ligado ao nível da mudança e
  formato de saída fixo. Governança da entrega incorporada ao `auditor-entrega`.

### Prova e projeto público

- `scripts/validar.py`: referências §, subseções e itens da pauta, caminhos, links, roteamento,
  cabeçalho e modelo dos agentes, segredos. `tests/test_validar.py` planta cada defeito e exige a
  reprovação.
- CI com actions fixadas por SHA e varredura de segredo no histórico inteiro (gitleaks).
- `evals/`: cenários rodados com e sem a skill, com comportamento, disparo da skill e custo.
- `exemplos/exemplo-completo.md`: o fluxo de uma mudança do pedido ao relatório.
- `templates/`: `AGENTS.md` de projeto (camada quente), ADR, relatório, questionário, manifesto de
  agente.
- Licença separada: texto em CC BY 4.0 (`LICENSE`), código em MIT (`LICENSE-CODE`). Cópias obtidas
  antes desta versão, publicadas sob MIT, continuam sob MIT.
- `CONTRIBUTING.md`, `SECURITY.md`, modelos de issue e de PR.
- Fontes externas reunidas em `references/fontes.md`.
