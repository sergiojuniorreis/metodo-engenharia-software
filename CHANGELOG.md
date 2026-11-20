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

### Dívida conhecida

- §16.6 (`front-end.md`), seção "Pauta §14.6": a descrição ao lado dos números dos itens não bate
  com a pauta (ex.: item 2 é isolamento por dono, item 6 é a mesma régua em todos os modos).
  Corrigir na próxima versão.
