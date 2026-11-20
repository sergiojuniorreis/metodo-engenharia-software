# Changelog

Formato: [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/). Versão: [SemVer](https://semver.org/lang/pt-BR/).
Mudança que quebra quem já usa o método (seção removida, regra que muda de sentido, caminho que
muda) sobe o primeiro número.

## [Não lançado]

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
  versão de biblioteca; Turbopack e Auth.js na tabela de front-end.
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
