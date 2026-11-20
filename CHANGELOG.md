# Changelog

Formato: [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/). Versão: [SemVer](https://semver.org/lang/pt-BR/).

## [Não lançado]

### Adicionado

- **Especialidades (§17)** em `references/17-especialidades/`: arquitetura e desenho de sistema,
  full stack, ciência e engenharia de dados, IA aplicada (LLM, RAG, busca semântica, banco
  vetorial, agentes), DevOps e SRE, cibersegurança, governança de software, dados e IA, qualidade e
  testes.
- **Nove agentes de desenvolvimento** em `agents/`, um por frente, com o fluxo, as devoluções e a
  coordenação entre agentes em `agents/README.md`.
- **Escada de componentes** e **ordem do trabalho de desempenho** no §10: cada componente de
  infraestrutura entra só diante de um gargalo medido.
- **Modelos** em `templates/`: `AGENTS.md` de projeto, ADR, relatório da entrega (§14.5) e
  questionário ao dono.
- **Validação do repositório** (`scripts/validar.py` e CI): referências §, caminhos citados,
  cabeçalho dos agentes e varredura de segredo.
- **Microsserviços e sistemas poliglotas** no §17.1: quando separar, regras depois de separar,
  contrato entre linguagens e formas de ligá-las (fila, HTTP/gRPC, subprocesso, extensão nativa).
- **Java/Kotlin e C#/.NET** para backend na tabela de linguagens do §3; Rust também como extensão
  nativa do Python no trecho quente medido.
- **Manifesto de agente do produto** (§16.2, "Um agente, uma função, um arquivo") e o modelo
  `templates/agente-produto.modelo.yaml`.
- **§16.5 aprofundado**: mobile (versão antiga em uso, loja, offline, permissões, assinatura),
  desktop (atualização assinada, multiplataforma, dado local) e API pública.
- **Contexto sem desperdício (§18)**: cache de conhecimento do projeto em três camadas — quente
  (`AGENTS.md`), morna (arquivos apontados) e fria (código) — com invalidação no mesmo commit e
  regras de leitura sem desperdício. `templates/AGENTS.modelo.md` reescrito como camada quente.
- Validador confere que todo arquivo de `references/` está roteado no `SKILL.md`, e vice-versa.
- `CHANGELOG.md`.
- Campos de norma exigida e de provedores de IA autorizados no `PERFIL.modelo.md`; termos novos no
  vocabulário (§15).

### Alterado

- `SKILL.md`: descrição, índice e tabela de situações cobrem as especialidades e os agentes; regra
  de ouro 4 inclui a escada de componentes.
- §6 aponta para o §17.4; §14.4 aponta para os agentes prontos.
- **Licença trocada de MIT para CC BY 4.0**, com autor e sugestão de atribuição no README. Cópias
  obtidas antes desta versão continuam sob MIT.
- `README.md`: badges, mapa, estrutura e índices cobrem especialidades, agentes e modelos;
  instalação copia também `agents/` e `templates/`, com versão em PowerShell.
- `.gitignore`: ignora `docs/` (material local) e mais padrões de credencial.

- **Carga mais leve do método**: o §14 mantém só o essencial e um resumo de uma linha por item
  da pauta; o detalhe da pauta foi para `14-6-pauta-seguranca.md` e §14.3/§14.4 para
  `14-3-4-ferramenta-agentes.md`, lidos só quando aplicáveis. As fontes externas foram reunidas em
  `references/fontes.md`. O `SKILL.md` tem uma tabela única de roteamento.

### Corrigido

- §16.6 (`front-end.md`): a seção "Pauta §14.6" agora descreve cada item como a pauta o define;
  referência quebrada "§SKILL" e número sem fonte sobre ferramentas de acessibilidade removidos.
