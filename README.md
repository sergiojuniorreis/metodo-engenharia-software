<div align="center">

# Método de Engenharia de Software

**Uma skill modular para agentes de IA e equipes de desenvolvimento: como se trabalha, como se decide e o que se considera entregue.**

[![Licença: CC BY 4.0](https://img.shields.io/badge/licen%C3%A7a-CC%20BY%204.0-lightgrey.svg)](LICENSE)
[![Idioma: pt-BR](https://img.shields.io/badge/idioma-pt--BR-009c3b.svg)](#)
[![Formato: SKILL.md](https://img.shields.io/badge/formato-SKILL.md-8a2be2.svg)](SKILL.md)
[![Especialidades: 8](https://img.shields.io/badge/especialidades-8-orange.svg)](#especialidades-references17-especialidades)
[![Agentes: 9](https://img.shields.io/badge/agentes-9-blue.svg)](agents/README.md)
[![validar](https://github.com/sergiojuniorreis/metodo-engenharia-software/actions/workflows/validar.yml/badge.svg)](https://github.com/sergiojuniorreis/metodo-engenharia-software/actions/workflows/validar.yml)

*Regra sem teste é boato.*

</div>

---

## O que é

Um método de engenharia para **todo projeto novo e todo reparo de código ou de arquitetura**,
com ou sem IA: sistemas, ERPs, automações, aplicativos, integrações, centrais de agentes
(orquestração), agentes com MCP, agentes conectados a Microsoft 365 / Google Workspace e
extensões de navegador.

Ele foi escrito no formato **skill** (`SKILL.md` + `references/`), para ser carregado por um
agente de IA. Também funciona como guia para pessoas: as regras são as mesmas para quem
escreve o código, seja gente ou modelo.

O método cobre:

- **Estudo de abordagem antes do código**: oito perguntas, pre-mortem, modelagem de ameaça e
  as **quatro análises do escopo** (paradigma de IA, rede neural, linear ou não linear,
  movimentos assíncronos).
- **Definição de pronto com evidência**: cada dimensão tem a prova que a demonstra.
- **Idempotência, concorrência, memória com TTL, observabilidade, release e rollback.**
- **Escada de componentes**: comece simples, ache o gargalo, ponha o menor componente que o
  resolve e repita. Banco, fila, cache e framework não entram por padrão.
- **Dados pessoais e fronteira de confiança**: entrada de fora é hostil até prova em contrário.
- **O portão do §14**: seis exigências para toda alteração de código, incluindo a pauta de
  segurança com 15 itens.
- **Oito especialidades** — arquitetura, full stack, ciência de dados, IA aplicada (RAG, busca
  semântica, agentes), DevOps/SRE, cibersegurança, governança, qualidade e testes — e **nove
  agentes de desenvolvimento** que as aplicam.

> De um projeto para outro muda o domínio, não o método.

### As oito regras de ouro

Se nada mais for lido, que se leia isto (do [`SKILL.md`](SKILL.md)):

1. **Nenhum projeto começa pelo código**: começa pelo estudo de abordagem (§3).
2. **O núcleo roteia, o domínio decide, a IA só veta**, em toda decisão com efeito
   financeiro, fiscal, legal ou cadastral.
3. **Regra sem teste é boato.**
4. **Nada é obrigatório por padrão**: comece simples, ache o gargalo, ponha o menor componente
   que o resolve e repita (§10).
5. **Operação que escreve é idempotente, com teto e freio.**
6. **Log completo, sem desistência silenciosa.**
7. **Dado pessoal e segredo não cruzam fronteira sem ofuscação** (§11).
8. **Não invente número.** "Não medi" é resposta; número inventado é defeito.

---

## Mapa da skill

O `SKILL.md` é o **núcleo**: o agente sempre o lê inteiro. O resto fica em `references/` e só
é carregado quando a situação pede. Assim o contexto fica enxuto.

```mermaid
flowchart TD
    N["<b>SKILL.md</b> (núcleo)<br/>Como carregar · Como usar · 8 regras de ouro<br/>Portão resumido · §2 Regras · §13 Conduta"]
    P["PERFIL.modelo.md<br/><i>contexto opcional da equipe</i>"]

    subgraph REF["references/ (carregado sob demanda)"]
        R3["§3 Estudo de abordagem<br/>4 análises do escopo · reparo"]
        R45["§4 Pronto · §5 Ciclo de IA"]
        R67["§6 RAG e veto · §7 Ferramentas e MCP"]
        R8["§8 Estado, concorrência e memória"]
        R910["§9 Observabilidade · §10 Escada de componentes"]
        R1112["§11 Dados pessoais · §12 Segurança e ritual"]
        R14["§14 Portão de toda alteração<br/>§14.6 Pauta de segurança"]
        R15["§15 Vocabulário"]
    end

    subgraph MOD["references/16-modulos/ (por tipo de projeto)"]
        M1["§16.1 ERP e sistemas transacionais"]
        M2["§16.2 Central de agentes e MCP"]
        M3["§16.3 Apps Microsoft, Google e afins"]
        M4["§16.4 Extensões de navegador"]
        M5["§16.5 Aplicativos web, mobile, desktop"]
        M6["§16.6 Front-end: interface, desempenho, acessibilidade"]
    end

    subgraph ESP["references/17-especialidades/ (por disciplina)"]
        E1["§17.1 Arquitetura · §17.2 Full stack"]
        E2["§17.3 Dados · §17.4 IA aplicada"]
        E3["§17.5 DevOps/SRE · §17.6 Cibersegurança"]
        E4["§17.7 Governança · §17.8 Qualidade e testes"]
    end

    AG["agents/<br/>9 agentes de desenvolvimento"]
    TP["templates/<br/>AGENTS.md · ADR · relatório · questionário · manifesto de agente"]

    N --> REF
    N --> MOD
    N --> ESP
    ESP --> AG
    P -. complementa .-> N
    TP -. modelos .-> N
```

<details>
<summary>Estrutura de arquivos (texto)</summary>

```
metodo-engenharia-software/
├── SKILL.md                         ← núcleo: sempre lido inteiro
├── PERFIL.modelo.md                 ← modelo opcional de perfil da equipe/projeto
├── references/
│   ├── 03-estudo-de-abordagem.md
│   ├── 04-05-pronto-e-ciclo-ia.md
│   ├── 06-07-ia-ferramentas-mcp.md
│   ├── 08-estado-memoria.md
│   ├── 09-10-observabilidade-ferramentas.md
│   ├── 11-12-dados-seguranca-ritual.md
│   ├── 14-portao.md                 ← portão + resumo da pauta
│   ├── 14-3-4-ferramenta-agentes.md
│   ├── 14-6-pauta-seguranca.md      ← detalhe da pauta, por item
│   ├── 15-vocabulario.md
│   ├── 18-contexto-cache.md         ← cache de conhecimento do projeto
│   ├── fontes.md                    ← todas as fontes externas
│   ├── 16-modulos/
│   │   ├── erp.md
│   │   ├── orquestracao-mcp.md
│   │   ├── apps-microsoft-google.md
│   │   ├── extensoes-navegador.md
│   │   ├── aplicativos.md
│   │   └── front-end.md
│   └── 17-especialidades/
│       ├── arquitetura.md
│       ├── full-stack.md
│       ├── dados.md
│       ├── ia-aplicada.md
│       ├── devops-sre.md
│       ├── ciberseguranca.md
│       ├── governanca.md
│       └── qualidade-testes.md
├── agents/                          ← 9 agentes + README com o fluxo
├── templates/                       ← AGENTS.md de projeto, ADR, relatório, questionário, manifesto de agente
├── scripts/validar.py               ← validação do repositório (roda na CI)
├── .github/workflows/validar.yml
├── CHANGELOG.md
├── README.md
└── LICENSE
```

</details>

---

## Índice dos módulos

### Núcleo

| Arquivo | Conteúdo |
|---|---|
| [`SKILL.md`](SKILL.md) | Como carregar, tabela "situação → seção", as oito regras de ouro, o portão resumido, **§2 Regras que valem sempre** (julgamento, arquitetura, anti-desculpas, sinais de alerta) e **§13 Conduta de trabalho** com o dono do projeto |
| [`PERFIL.modelo.md`](PERFIL.modelo.md) | Modelo opcional. Idioma, shell, moeda, lei de dados, cofre de segredos, norma exigida, provedores de IA autorizados, linhas de trabalho e regras do domínio ficam aqui, nunca no núcleo |

### Referências (`references/`)

| § | Arquivo | Quando carregar | Destaques |
|---|---|---|---|
| §3 | [`03-estudo-de-abordagem.md`](references/03-estudo-de-abordagem.md) | Projeto novo, mudança de rumo, reparo de arquitetura | As oito perguntas · conduta sênior (pre-mortem, STRIDE, funções de aptidão) · **as quatro análises do escopo** · da forma do problema à linguagem · reparo (cerca de Chesterton, teste de caracterização, figueira estranguladora) · fontes externas |
| §4 · §5 | [`04-05-pronto-e-ciclo-ia.md`](references/04-05-pronto-e-ciclo-ia.md) | "Está pronto para entregar?" · construir skill, agente ou RAG | Tabela "pronto quando × evidência que prova" · ciclo de IA em 13 passos · qualidade de toda entrega |
| §6 · §7 | [`06-07-ia-ferramentas-mcp.md`](references/06-07-ia-ferramentas-mcp.md) | RAG, prompt de decisão, ferramenta/MCP, automação que grava em sistema alheio | Fonte primária manda · schema antes da regra · citação literal conferida · uma ferramenta = um verbo · circuit breaker · raio de explosão e freio · provar o fallback |
| §8 | [`08-estado-memoria.md`](references/08-estado-memoria.md) | Dado compartilhado, retomada, cache, memória do sistema | Escrita condicional · máquina de estados explícita · cinco cortes de retomada · memória com origem, versão da regra, TTL e lápide |
| §9 · §10 | [`09-10-observabilidade-ferramentas.md`](references/09-10-observabilidade-ferramentas.md) | Log, métrica, alerta, custo · vai entrar banco, fila, cache, container · desempenho | Identificador por execução · custo como métrica · tabela "entra quando × não entra, use isto" · **escada de componentes** · ordem do trabalho de desempenho · dimensionamento por gatilho medido |
| §11 · §12 | [`11-12-dados-seguranca-ritual.md`](references/11-12-dados-seguranca-ritual.md) | Dado pessoal, documento de cliente, entrada de fora · produção, release, incidente | Minimização · ofuscação antes do modelo · entrada hostil (inclusive a saída do modelo) · ritual de mudança |
| §14 | [`14-portao.md`](references/14-portao.md) | **Toda alteração de código, antes da primeira edição** | Auditoria total (mapa de impacto + diff hunk a hunk) · âncora contra drift · relatório da entrega · **resumo da pauta de segurança (15 itens)** |
| §14.3 · §14.4 | [`14-3-4-ferramenta-agentes.md`](references/14-3-4-ferramenta-agentes.md) | A mudança traz ferramenta nova ou se cogita usar agentes | Teste de necessidade e passo a passo de configuração · agentes com orçamento |
| §14.6 | [`14-6-pauta-seguranca.md`](references/14-6-pauta-seguranca.md) | Itens da pauta que se aplicam à mudança | Detalhe e evidência exigida de cada item |
| §15 | [`15-vocabulario.md`](references/15-vocabulario.md) | Dúvida sobre um termo | Núcleo, skill, setor, corpus, bateria, veto, lápide, ADR, drift, outbox, saga, RAG, embedding, SLO, entre outros |
| §18 | [`18-contexto-cache.md`](references/18-contexto-cache.md) | Preparar o `AGENTS.md` do projeto; tarefa gastando contexto com o que já se sabe | Cache de conhecimento em três camadas (quente, morna, fria) · invalidação · leitura sem desperdício |
| — | [`fontes.md`](references/fontes.md) | Conferir de onde vem uma regra | Todas as fontes externas, por seção |

### Módulos por tipo de projeto (`references/16-modulos/`)

| § | Arquivo | Carregue quando |
|---|---|---|
| §16.1 | [`erp.md`](references/16-modulos/erp.md) | O projeto customiza, integra ou automatiza um ERP ou outro sistema transacional (financeiro, fiscal, estoque, pedidos) |
| §16.2 | [`orquestracao-mcp.md`](references/16-modulos/orquestracao-mcp.md) | O produto tem vários agentes coordenados, um orquestrador, ou cria/consome servidores MCP |
| §16.3 | [`apps-microsoft-google.md`](references/16-modulos/apps-microsoft-google.md) | O agente lê ou escreve em e-mail, calendário, documentos, chat ou arquivos de uma suíte de escritório |
| §16.4 | [`extensoes-navegador.md`](references/16-modulos/extensoes-navegador.md) | O projeto é uma extensão, um userscript ou um agente que navega e clica |
| §16.5 | [`aplicativos.md`](references/16-modulos/aplicativos.md) | O projeto tem interface para usuário final ou API pública: mobile (versão antiga que vive para sempre, loja, offline), desktop (atualização assinada, multiplataforma) e API pública |
| §16.6 | [`front-end.md`](references/16-modulos/front-end.md) | O projeto tem interface web: renderização, orçamento de bundle, Core Web Vitals, arquitetura de componentes, acessibilidade e a stack de referência |

### Especialidades (`references/17-especialidades/`)

Cada setor diz **como fazer bem uma disciplina** e aponta para as regras do núcleo, sem repeti-las.

| § | Arquivo | Carregue quando |
|---|---|---|
| §17.1 | [`arquitetura.md`](references/17-especialidades/arquitetura.md) | Desenhar sistema, fronteira, contrato, API ou modelo de dados; microsserviços; sistemas com mais de uma linguagem |
| §17.2 | [`full-stack.md`](references/17-especialidades/full-stack.md) | Implementar backend, API, banco ou a ligação com a interface |
| §17.3 | [`dados.md`](references/17-especialidades/dados.md) | Métrica, painel, previsão, classificação, pipeline de dados |
| §17.4 | [`ia-aplicada.md`](references/17-especialidades/ia-aplicada.md) | LLM, RAG, banco vetorial, busca semântica, agentes, avaliação e custo de IA |
| §17.5 | [`devops-sre.md`](references/17-especialidades/devops-sre.md) | CI/CD, infraestrutura, deploy, SLO, alerta, backup e recuperação |
| §17.6 | [`ciberseguranca.md`](references/17-especialidades/ciberseguranca.md) | Modelagem de ameaça, varredura de segredo, dependências, texto que sai |
| §17.7 | [`governanca.md`](references/17-especialidades/governanca.md) | ADR, dívida, dados pessoais, governança de IA, licenças, evidência de auditoria |
| §17.8 | [`qualidade-testes.md`](references/17-especialidades/qualidade-testes.md) | Que teste prova o quê, mutação, matriz de interrupção, revisão de código |

> **Projeto sem IA:** §5, §6, as análises A e B do §3, os módulos §16.2 a §16.4 e o §17.4 se
> respondem "não se aplica — motivo". O resto vale inteiro.

### Agentes de desenvolvimento (`agents/`)

Nove especialistas para o Claude Code, um por frente. Quem audita não edita: devolve ao
responsável com a evidência. Fluxo, devoluções e coordenação em [`agents/README.md`](agents/README.md).

| Agente | Frente |
|---|---|
| `consultor-dominio` | Problema, requisitos em número, casos reais, questionário ao dono |
| `arquiteto-software` | Onde cada regra mora, menor desenho que atende, mapa de impacto |
| `cientista-dados` | Métrica, dado, base simples, avaliação sem vazamento |
| `engenheiro-ia-aplicada` | Escada de IA, desenho híbrido, RAG, agentes, custo |
| `engenheiro-full-stack` | Implementação com o menor diff e teste vermelho → verde |
| `engenheiro-devops-sre` | Pipeline, infraestrutura, deploy, observabilidade, rollback |
| `especialista-seguranca` | Modelagem de ameaça, pauta §14.6, varreduras |
| `guardiao-governanca` | ADR, dívida, inventários de dados e de IA, licenças, evidência |
| `auditor-entrega` | Portão final: CI em cópia limpa, mutação, relatório §14.5 |

### Modelos (`templates/`)

| Arquivo | Para quê |
|---|---|
| [`AGENTS.modelo.md`](templates/AGENTS.modelo.md) | Regras do projeto para os agentes: invariantes, setores, testes, versão, segredos |
| [`adr.md`](templates/adr.md) | Registro de decisão com alternativas, consequências e gatilho de revisão |
| [`relatorio-entrega.md`](templates/relatorio-entrega.md) | O relatório do §14.5, pronto para preencher |
| [`questionario-dono.md`](templates/questionario-dono.md) | Perguntas ao dono do domínio, com o padrão "sem resposta, vale X" |
| [`agente-produto.modelo.yaml`](templates/agente-produto.modelo.yaml) | Manifesto de um agente do produto: função, schemas, ferramentas, permissões, tetos (§16.2) |

---

## Como usar

Escolha o cenário. Nos três, a pasta precisa manter a estrutura acima, porque o `SKILL.md`
aponta para `references/`, `agents/` e `templates/` por caminho relativo.

### 1. Como skill no Claude Code, no Abacus.AI (DeepAgent) ou em outro agente com suporte a skills

O agente lê o nome e a descrição do `SKILL.md` para decidir quando usar a skill. Depois lê o
núcleo inteiro e só abre as referências que a tarefa pede.

**Passo a passo:**

1. Baixe o repositório:
   ```bash
   git clone https://github.com/sergiojuniorreis/metodo-engenharia-software.git
   ```
2. Copie os arquivos da skill para a pasta de skills do agente, numa pasta com o mesmo nome do
   campo `name` do `SKILL.md`:
   ```bash
   mkdir -p skills/metodo-engenharia-software
   cp -r metodo-engenharia-software/SKILL.md \
         metodo-engenharia-software/PERFIL.modelo.md \
         metodo-engenharia-software/references \
         metodo-engenharia-software/agents \
         metodo-engenharia-software/templates \
         skills/metodo-engenharia-software/
   ```
   `README.md`, `LICENSE`, `CHANGELOG.md`, `scripts/` e `.github/` servem ao repositório e não
   precisam ir para a pasta da skill.
3. **No Abacus.AI / DeepAgent:** envie os arquivos na conversa (ou informe a URL deste
   repositório) e peça *"crie uma skill chamada `metodo-engenharia-software` a partir destes
   arquivos, usando a descrição do frontmatter do `SKILL.md`"*. O agente registra a skill e
   ela passa a valer nas próximas conversas.
4. **Em outros agentes compatíveis com o formato `SKILL.md`:** coloque a pasta no diretório
   de skills que o agente lê (por exemplo, `~/.claude/skills/` no Claude Code).
5. **Agentes (Claude Code):** copie os arquivos de `agents/`, menos o `README.md`, para
   `~/.claude/agents/` (todos os projetos) ou `.claude/agents/` (um projeto).
6. *(Opcional)* Copie `PERFIL.modelo.md` para `PERFIL.md` dentro da pasta da skill e preencha
   idioma, shell, moeda, lei de dados e regras do seu domínio.

#### Instalação por terminal (Linux, macOS, Claude Code, Codespaces)

Cole o comando abaixo no terminal. Ele clona o repositório, instala a skill em
`~/.claude/skills/` e os agentes em `~/.claude/agents/`:

```bash
git clone --depth 1 https://github.com/sergiojuniorreis/metodo-engenharia-software.git /tmp/mes \
  && mkdir -p ~/.claude/skills/metodo-engenharia-software ~/.claude/agents \
  && cp -r /tmp/mes/SKILL.md /tmp/mes/PERFIL.modelo.md /tmp/mes/references \
        /tmp/mes/agents /tmp/mes/templates ~/.claude/skills/metodo-engenharia-software/ \
  && find /tmp/mes/agents -name '*.md' ! -name README.md -exec cp {} ~/.claude/agents/ \; \
  && rm -rf /tmp/mes \
  && echo "Skill e agentes instalados em ~/.claude"
```

**PowerShell (Windows):**

```powershell
$tmp = Join-Path $env:TEMP 'mes'
git clone --depth 1 https://github.com/sergiojuniorreis/metodo-engenharia-software.git $tmp
$skill = Join-Path $HOME '.claude\skills\metodo-engenharia-software'
$agentes = Join-Path $HOME '.claude\agents'
New-Item -ItemType Directory -Force $skill, $agentes | Out-Null
Copy-Item -Recurse -Force "$tmp\SKILL.md", "$tmp\PERFIL.modelo.md", "$tmp\references", "$tmp\agents", "$tmp\templates" $skill
Get-ChildItem "$tmp\agents\*.md" -Exclude README.md | Copy-Item -Destination $agentes -Force
Remove-Item -Recurse -Force $tmp
```

> **Codespaces:** o diretório `~/.claude/` é lido pelo Claude Code dentro do Codespace. Se o
> seu agente usa outro caminho (por exemplo um diretório `skills/` na raiz do projeto), troque o
> destino pelo caminho que ele lê.

**Conferir a instalação:**

```bash
ls ~/.claude/skills/metodo-engenharia-software
# deve listar: PERFIL.modelo.md  SKILL.md  agents  references  templates
ls ~/.claude/agents
# deve listar os 9 agentes
```

**Atualizar depois:** repetir o mesmo comando sobrescreve com a versão mais recente. Se
preferir manter um clone versionado:

```bash
git clone https://github.com/sergiojuniorreis/metodo-engenharia-software.git
cd metodo-engenharia-software && git pull   # nas próximas vezes
```

**Como conferir que funcionou:** peça ao agente *"vou começar um projeto novo de integração
com ERP"*. Uma skill carregada responde pelo **estudo de abordagem (§3)** e pelo **módulo
§16.1** antes de propor qualquer código. Se ele for direto para o código, a skill não
disparou.

### 2. Como system prompt concatenado (LLMs sem suporte a pastas)

Para modelos que só aceitam texto (API de chat, `AGENTS.md`, arquivo de regras do editor,
GPT personalizado), junte o núcleo com as referências da situação num único arquivo.

**Prompt completo** (todas as seções):

```bash
cd metodo-engenharia-software
{ cat SKILL.md; for f in references/*.md references/16-modulos/*.md references/17-especialidades/*.md; do
    printf '\n\n---\n\n<!-- %s -->\n\n' "$f"; cat "$f"; done; } > prompt-completo.md
```

**Prompt enxuto** (núcleo + o que o projeto usa). Exemplo para um projeto de agente com MCP e RAG:

```bash
cat SKILL.md references/14-portao.md references/03-estudo-de-abordagem.md \
    references/06-07-ia-ferramentas-mcp.md references/16-modulos/orquestracao-mcp.md \
    references/17-especialidades/ia-aplicada.md > prompt-agente-mcp.md
```

**PowerShell (Windows):**

```powershell
Set-Location metodo-engenharia-software
$arquivos = @('SKILL.md') + (Get-ChildItem references\*.md, references\16-modulos\*.md, references\17-especialidades\*.md).FullName
Get-Content $arquivos -Encoding UTF8 | Set-Content prompt-completo.md -Encoding UTF8
```

Depois cole o arquivo gerado no campo de system prompt ou salve como `AGENTS.md` (ou o
equivalente da sua ferramenta) na raiz do projeto.

**Regras para escolher o que concatenar:**

- O `SKILL.md` vai **sempre**.
- O **§14 (`14-portao.md`)** vai sempre que o modelo for alterar código.
- Inclua os módulos do §16 que correspondem ao tipo de projeto e as especialidades do §17 que a
  tarefa toca.
- Prompt longo custa token em toda chamada. Se a janela ou o orçamento apertarem, use a
  versão enxuta.

### 3. Como referência metodológica (sem IA)

O método também funciona como guia de equipe, checklist de revisão e base de onboarding.

| Momento | O que ler | O que produzir |
|---|---|---|
| Kickoff de projeto | §3 inteiro e §17.1 | Estudo de abordagem de meia página com as quatro análises e os ADRs da stack ([modelo](templates/adr.md)) |
| Antes de cada alteração | §14.1, §14.2 e §14.6 | Mapa de impacto, âncora (objetivo, aceite, escopo, invariantes, Fora) e pauta de segurança respondida |
| Revisão de PR | §14.5, §17.8 e "Sinais de alerta" do §2 | Relatório da entrega com evidência por item ([modelo](templates/relatorio-entrega.md)) |
| "Posso entregar?" | §4 | Tabela de pronto preenchida, com a evidência ao lado de cada linha |
| Incidente ou release | §12 e §17.5 | Ritual de mudança, release arquivada com rollback registrado e incidente fechado com teste novo |
| Auditoria ou conformidade | §17.7 | Pacote de evidência da release, inventários de dados pessoais e de usos de IA |
| Onboarding | `SKILL.md` + §15 | Vocabulário comum da equipe |

**Sugestão:** adote o método por partes. Comece pelo §14 (portão) e pelo §4 (pronto). São os
que mais pegam defeito com menos esforço.

---

## Adaptando ao seu contexto

- **Regra do repositório vence a do método.** Se o seu projeto tem convenção própria, ela
  prevalece, e a divergência deve ser dita em voz alta, não resolvida no silêncio. Use o
  [`templates/AGENTS.modelo.md`](templates/AGENTS.modelo.md) para escrevê-la.
- **O `AGENTS.md` é o cache quente do projeto** (§18): curto, só fatos que quase toda tarefa
  usa, carregado em toda sessão pelo `CLAUDE.md` (`@AGENTS.md`). O detalhe fica em arquivos
  apontados por ele, lidos só quando o assunto aparece. Assim o agente não redescobre o que o
  projeto já sabe e não paga contexto pelo que a tarefa não usa.
- **Contexto vai no `PERFIL.md`, não no núcleo.** Palavras de domínio, idioma, moeda e lei de
  dados (LGPD, GDPR ou outra) ficam no perfil. Assim o núcleo continua genérico e pode ser
  atualizado sem conflito.
- **Projeto sem IA** responde as seções de IA com "não se aplica — motivo". Fora isso, o
  método vale inteiro.

---

## Validar

```bash
python scripts/validar.py
```

Confere que toda referência § existe, que todo caminho e link citado existe, que o cabeçalho dos
agentes está correto e que nenhum padrão de chave entrou no repositório. Código de saída 0 é tudo
certo. A mesma verificação roda na CI a cada push. Mudanças em [`CHANGELOG.md`](CHANGELOG.md).

---

## Contribuindo

Contribuições são bem-vindas, com uma condição: **elas seguem o próprio método.**

1. **Abra uma issue antes do PR** descrevendo o problema: o que a regra atual deixa passar, ou
   onde ela atrapalha, com um caso real (mascarado, sem dado pessoal nem de cliente).
2. **Uma mudança por PR**, dentro de um único arquivo ou seção sempre que possível
   (*setores nomeados*, §2).
3. **Regra nova vem com o motivo e a evidência:** o caso que ela teria pego, a fonte que a
   sustenta ou o teste que a comprova. *Regra sem teste é boato.*
4. **Não quebre a estrutura:** o `SKILL.md` continua sendo o núcleo, o detalhe vai para
   `references/` e a tabela "Como carregar" é atualizada no mesmo commit.
5. **Zero palavra de domínio no núcleo.** Regra específica de um setor ou tipo de projeto vai
   para um módulo do §16, uma especialidade do §17 ou o `PERFIL.modelo.md`.
6. **`python scripts/validar.py` verde** antes do PR, e o `CHANGELOG.md` atualizado.
7. **Português do Brasil**, tom direto, sem jargão desnecessário.

---

## Autor e licença

Criado por **Sergio Volney dos Reis Junior** — [github.com/sergiojuniorreis](https://github.com/sergiojuniorreis).

Distribuído sob a licença
[**Creative Commons Atribuição 4.0 Internacional (CC BY 4.0)**](LICENSE): você pode usar,
adaptar e redistribuir, inclusive comercialmente, desde que cite o autor, inclua o link da
licença e indique se fez alterações.

Sugestão de atribuição:

> *Método de Engenharia de Software*, de Sergio Volney dos Reis Junior
> (github.com/sergiojuniorreis/metodo-engenharia-software), licenciado sob CC BY 4.0.

---

<div align="center">

**Se este método evitou um defeito em produção, deixe uma ⭐ no repositório.**

</div>
