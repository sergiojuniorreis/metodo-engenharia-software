# §17.9 — Ferramentas de prova por linguagem

Carregue quando uma exigência do método pede evidência de ferramenta — teste, mutação, análise
estática, auditoria de dependências, varredura de segredo — e é preciso saber **qual comando
roda**. A tabela é um menu, não uma obrigação: ferramenta entra pelo §14.3, com versão fixada no
projeto, e o que já existe no repositório vence a sugestão daqui.

| Prova | Python | TypeScript / JavaScript | Java / Kotlin | Go | C# / .NET | Rust |
|---|---|---|---|---|---|---|
| Teste | `python -m pytest` | `npm test` (Vitest ou Jest) | `mvn -B verify` ou `./gradlew test` (JUnit 5) | `go test ./...` | `dotnet test` | `cargo test` |
| Cobertura | `pytest --cov` (coverage.py) | `vitest --coverage` | JaCoCo | `go test -cover ./...` | coverlet | cargo-llvm-cov |
| Mutação (§17.8) | mutmut | StrykerJS | PIT | go-mutesting | Stryker.NET | cargo-mutants |
| Lint e formatação | `ruff check` · `ruff format` | ESLint · Prettier | Spotless · ktlint | `go vet` · `gofmt` · staticcheck | `dotnet format` | `cargo clippy` · `cargo fmt` |
| Análise estática de segurança | bandit ou Semgrep | Semgrep | SpotBugs + FindSecBugs ou Semgrep | gosec | analisadores Roslyn ou Semgrep | `cargo clippy` + revisão de `unsafe` |
| Auditoria de dependências (§14.6 item 15) | `pip-audit` | `npm audit` | OWASP Dependency-Check | `govulncheck ./...` | `dotnet list package --vulnerable` | `cargo audit` |
| Tipos | mypy ou pyright | `tsc --noEmit` | compilador | compilador | compilador | compilador |
| Segredo no histórico (§14.6 item 9) | gitleaks | gitleaks | gitleaks | gitleaks | gitleaks | gitleaks |

## Como usar

- **Comando único** (§5): o projeto junta as provas que adotou num só comando (ex.: `make check`,
  `npm run check`, script na raiz), o mesmo local e na CI.
- **Nível trivial**: teste e lint. **Padrão**: mais tipos e auditoria de dependências na CI.
  **Alto risco**: mais mutação nas guardas novas e análise estática de segurança (§14.0).
- **Mutação é cara**: rode só sobre os arquivos da mudança, não sobre o projeto inteiro.
- **Ferramenta que não existe no projeto** entra com o passo a passo do §14.3; até lá, a linha do
  relatório diz "não se aplica — ferramenta não adotada" e a dívida fica registrada.
- **Kit de início** (`scripts/iniciar_projeto.py`) já cria a CI com teste e gitleaks para a
  linguagem escolhida. Em Python e TypeScript, cria também o lint e a formatação, que rodam na CI
  antes do teste, com o passo a passo do §14.3 em `docs/lint-e-formatacao.md`:
  - Python: `ruff.toml`, com ruff 0.17.6.
  - TypeScript: `eslint.config.mjs`, `.prettierrc.json` e `.prettierignore`, com ESLint 10.15.0,
    typescript-eslint 8.74.0, TypeScript 6.0.3 e Prettier 3.10.1, versões conferidas em 2026-11-24.
  - As outras linguagens usam o lint da tabela acima, adotado pelo §14.3.
- **Lint no trabalho dos agentes**: o `engenheiro-full-stack` roda o lint na linha de base e a cada
  passo, e roda o Prettier só nos arquivos que tocou. O `arquiteto-software` escreve como regra de
  lint toda fronteira que dá para travar assim, como o import proibido do núcleo para o domínio. O
  `auditor-entrega` trata o lint como passo da régua.
- **Prettier mantém o fim de linha** (`"endOfLine": "auto"`). O Markdown dos modelos do método fica
  no `.prettierignore`, para a primeira CI não nascer vermelha. Formatar esse Markdown é um commit
  próprio, de nível trivial.
