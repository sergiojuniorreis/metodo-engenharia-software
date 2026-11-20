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
  linguagem escolhida.
