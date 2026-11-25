"""Kit de início de projeto: cria no repositório a estrutura que o método pressupõe.

Cria (sem sobrescrever o que já existe):
  AGENTS.md, CLAUDE.md                      camada quente do projeto (§18)
  docs/estudo-de-abordagem.md               §3, para preencher
  docs/adr/0001-registro-de-decisoes.md      primeiro ADR
  .github/workflows/ci.yml                  lint + teste da linguagem + segredo no histórico
  .gitignore                                segredos e lixo comum
  ruff.toml | eslint.config.mjs, .prettierrc.json, .prettierignore
  docs/lint-e-formatacao.md                 lint e formatação (Python e TypeScript), §14.3
e roda `git init` se a pasta ainda não é repositório.

Uso:
  python -I iniciar_projeto.py <pasta> --nome "Meu projeto" --linguagem python
Linguagens: python, typescript, java, go, csharp, rust, outra.
"""
import argparse
import subprocess
import sys
from pathlib import Path

RAIZ_METODO = Path(__file__).resolve().parent.parent
GITLEAKS = "gitleaks/gitleaks-action@e0c47f4f8be36e29cdc102c57e68cb5cbf0e8d1e # v3.0.0"
CHECKOUT = "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1"

TESTE = {
    "python": ["if [ -f requirements.txt ]; then python -m pip install -r requirements.txt; fi",
               "python -m pip install pytest==8.3.4", "python -m pytest"],
    "typescript": ["npm ci", "npm test"],
    "java": ["if [ -f mvnw ]; then ./mvnw -B verify; elif [ -f gradlew ]; then ./gradlew test; else mvn -B verify; fi"],
    "go": ["go vet ./...", "go test ./..."],
    "csharp": ["dotnet test"],
    "rust": ["cargo test"],
    "outra": ["echo 'Defina o comando de teste do projeto neste passo (§5, comando único)' && exit 1"],
}

# Lint e formatação (§17.9) rodam na CI antes do teste. Versões travadas e conferidas no registro
# em 2026-11-24; a troca de versão segue o §14.3 e o passo a passo em docs/lint-e-formatacao.md.
RUFF = "ruff==0.17.6"
NPM_LINT = ("eslint@10.15.0 @eslint/js@10.0.1 typescript-eslint@8.74.0 "
            "typescript@6.0.3 prettier@3.10.1")  # typescript-eslint 8.74 pede typescript <6.1
LINT = {
    "python": [f"python -m pip install {RUFF}", "ruff check .", "ruff format --check ."],
    "typescript": ["npm run lint"],
}

RUFF_TOML = """# Lint e formatação do projeto (§17.9). Passo a passo: docs/lint-e-formatacao.md.
line-length = 100

[lint]
# E/W estilo, F erros prováveis, I ordem dos imports, B armadilhas comuns, UP sintaxe antiga.
select = ["E", "F", "W", "I", "B", "UP"]
"""

ESLINT_CONFIG = """// Lint do projeto (§17.9). Passo a passo: docs/lint-e-formatacao.md.
// Formatação é do Prettier; o ESLint cuida de erro provável e de fronteira (no-restricted-imports).
import js from "@eslint/js";
import { defineConfig, globalIgnores } from "eslint/config";
import tseslint from "typescript-eslint";

export default defineConfig([
  globalIgnores(["dist/", "coverage/", "node_modules/"]),
  js.configs.recommended,
  tseslint.configs.recommended,
]);
"""

# endOfLine "auto": o Prettier mantém o fim de linha que o arquivo já tem (regra do full-stack).
PRETTIERRC = """{
  "printWidth": 100,
  "endOfLine": "auto"
}
"""

PRETTIERIGNORE = """dist/
coverage/
package-lock.json
# Markdown dos modelos do método: formatá-lo é commit próprio, de nível trivial. Para formatar,
# tire esta linha e rode `npm run format -- "**/*.md"` num commit só de formatação.
*.md
"""

GUIA_LINT_PY = f"""# ruff 0.17.6 — configuração

Para que serve aqui: lint (erro provável, import, armadilha) e formatação do Python, num binário só.
Por que não a alternativa: flake8 + isort + black são três ferramentas e três configurações.
Onde roda: na máquina do dev e na CI (`.github/workflows/ci.yml`), antes do teste.
Quem opera: quem altera código (`engenheiro-full-stack`); o auditor confere o código de saída.
Custo e licença: gratuito, MIT.

## Pré-requisitos

- Python 3 instalado: `python --version` (no Windows sem `python`, `py -3 --version`).

## Instalar

1. `python -m pip install {RUFF}` → termina com `Successfully installed ruff-0.17.6`.

## Configurar

- `ruff.toml` na raiz (já criado pelo kit): `line-length = 100` e as regras em `[lint] select`.
- Regra desligada numa linha só com motivo: `# noqa: E501 — <motivo>`. Sem motivo, não passa revisão.

## Conferir

- `ruff check .` → `All checks passed!`, código de saída 0.
- `ruff format --check .` → `N files already formatted`, código de saída 0.

## Outra máquina

- Repete-se o passo Instalar. `ruff.toml` e a CI vêm pelo repositório.

## Quando falhar

- `ruff: command not found` → o Scripts do Python fora do PATH → use `python -m ruff check .`.
- `ruff format --check` acusa arquivo → rode `ruff format <arquivo>` só nos arquivos que você tocou;
  reformatação do projeto inteiro é commit separado, nunca junto com mudança funcional.

## Desfazer

1. `python -m pip uninstall -y ruff`.
2. Apague `ruff.toml`, este arquivo e os três passos de ruff em `.github/workflows/ci.yml`.
3. Confira: `python -m ruff --version` falha com `No module named ruff`.
"""

GUIA_LINT_TS = f"""# ESLint 10.15.0 + Prettier 3.10.1 — configuração

Para que serve aqui: o ESLint acha erro provável e fronteira quebrada (import proibido); o Prettier
formata. Cada um faz uma coisa, sem regra de estilo brigando entre eles.
Por que não a alternativa: Biome junta os dois numa ferramenta; fica o par ESLint + Prettier porque é
o que o §16.6 do método já indica. Projeto que preferir Biome troca pelo §14.3.
Onde roda: na máquina do dev e na CI (`npm run lint`, antes do `npm test`).
Quem opera: quem altera código (`engenheiro-full-stack`); o auditor confere o código de saída.
Custo e licença: gratuitos, MIT (ESLint, typescript-eslint, Prettier) e Apache-2.0 (TypeScript).

## Pré-requisitos

- Node e npm: `node --version` e `npm --version`.
- `package.json` na raiz (`npm init -y`, se ainda não existe).

## Instalar

1. `npm install --save-dev --save-exact {NPM_LINT}`
   → `added N packages`, com as versões exatas em `devDependencies` e no `package-lock.json`.

## Configurar

- Já criados pelo kit: `eslint.config.mjs`, `.prettierrc.json` (`endOfLine: "auto"` mantém o fim
  de linha de cada arquivo) e `.prettierignore`.
- Em `package.json`, dentro de `"scripts"`:
  `"lint": "eslint . && prettier --check ."` e `"format": "prettier --write"`.
- Regra desligada numa linha só com motivo:
  `// eslint-disable-next-line <regra> -- <motivo>`. Sem motivo, não passa revisão.

## Conferir

- `npm run lint` → o ESLint não imprime nada e o Prettier diz
  `All matched files use Prettier code style!`; código de saída 0.

## Outra máquina

- `npm ci` instala tudo pelo `package-lock.json`. As configs e a CI vêm pelo repositório.

## Quando falhar

- `Cannot find package '@eslint/js'` → as dependências não foram instaladas → `npm ci`.
- O Prettier acusa arquivo → `npm run format -- <arquivos que você tocou>`; reformatação do projeto
  inteiro é commit separado, nunca junto com mudança funcional.

## Desfazer

1. `npm uninstall eslint @eslint/js typescript-eslint typescript prettier`.
2. Apague `eslint.config.mjs`, `.prettierrc.json`, `.prettierignore`, este arquivo e os scripts
   `lint` e `format` do `package.json`; tire o `npm run lint` de `.github/workflows/ci.yml`.
3. Confira: `npx --no-install eslint --version` falha.
"""

ARQUIVOS_LINT = {
    "python": {"ruff.toml": RUFF_TOML, "docs/lint-e-formatacao.md": GUIA_LINT_PY},
    "typescript": {"eslint.config.mjs": ESLINT_CONFIG, ".prettierrc.json": PRETTIERRC,
                   ".prettierignore": PRETTIERIGNORE, "docs/lint-e-formatacao.md": GUIA_LINT_TS},
}

GITIGNORE = """# Segredos e ambiente (§14.6 item 7)
.env
.env.*
*.pem
*.key
*.p12
# Contexto local
PERFIL.md
# Lixo comum
__pycache__/
node_modules/
target/
bin/
obj/
dist/
.DS_Store
Thumbs.db
"""

ADR = """# ADR-0001 — Registrar decisões de arquitetura

- **Data:** <AAAA-MM-DD>
- **Estado:** aceita
- **Porta:** duas vias

## Contexto

Decisões de uma via (esquema de dado, contrato público, runtime, distribuição) precisam ficar
escritas com o motivo, as alternativas descartadas e o gatilho que faria mudar de ideia (§2, §17.7).

## Decisão

Cada decisão de uma via vira um arquivo `docs/adr/NNNN-titulo.md` no mesmo commit da mudança,
no formato de `templates/adr.md` do método.

## Gatilho de revisão

Nenhum: é a regra do registro.
"""


FUMACA_PY = '''"""Teste de fumaça do kit: prova que a suíte roda. Troque pelo primeiro teste real (§14)."""


def test_a_suite_roda():
    assert True
'''

# Nas outras linguagens o teste depende do arquivo do projeto (package.json, go.mod, pom.xml,
# *.csproj, Cargo.toml). Até ele existir, a CI diz isso em voz alta e passa; depois, roda os testes.
ARQUIVO_DO_PROJETO = {
    "typescript": "package.json", "go": "go.mod", "rust": "Cargo.toml",
    "java": "pom.xml build.gradle build.gradle.kts", "csharp": "*.csproj *.sln",
}


def ci_yml(linguagem):
    comandos = TESTE[linguagem][:-1] + LINT.get(linguagem, []) + TESTE[linguagem][-1:]
    if linguagem in ARQUIVO_DO_PROJETO:
        teste = " && ".join(comandos)
        arquivos = ARQUIVO_DO_PROJETO[linguagem]
        comandos = [f"if ls {arquivos} >/dev/null 2>&1; then {teste}; "
                    f"else echo '::notice::ainda sem {arquivos.split()[0]}: crie o projeto e o primeiro teste'; fi"]
    # Bloco literal: comando com ": " (ex.: o ::notice::) em escalar simples quebra o YAML.
    passos = "\n".join(f"      - run: |\n          {cmd}" for cmd in comandos)
    return f"""name: ci

on:
  push:
  pull_request:

permissions:
  contents: read

jobs:
  testes:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: {CHECKOUT}
        with:
          fetch-depth: 0
{passos}
      - name: Segredo no histórico inteiro
        uses: {GITLEAKS}
        env:
          GITHUB_TOKEN: ${{{{ secrets.GITHUB_TOKEN }}}}
          GITLEAKS_ENABLE_COMMENTS: false
"""


def agents_md(nome, linguagem):
    modelo = (RAIZ_METODO / "templates" / "AGENTS.modelo.md").read_text(encoding="utf-8")
    fim_comentario = modelo.find("-->")
    if modelo.startswith("<!--") and fim_comentario != -1:
        modelo = modelo[fim_comentario + 3:].lstrip("\n")
    comando = " && ".join(TESTE[linguagem][-1:])
    return (modelo.replace("<Projeto>", nome)
            .replace("| Validar tudo (vale o código de saída) | `<comando>` |",
                     f"| Validar tudo (vale o código de saída) | `{comando}` |"))


def escrever(destino, rel, conteudo, criados, mantidos):
    p = destino / rel
    if p.exists():
        mantidos.append(rel)
        return
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(conteudo, encoding="utf-8", newline="\n")
    criados.append(rel)


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pasta")
    ap.add_argument("--nome", required=True)
    ap.add_argument("--linguagem", choices=sorted(TESTE), required=True)
    a = ap.parse_args(argv)
    destino = Path(a.pasta).resolve()
    destino.mkdir(parents=True, exist_ok=True)
    criados, mantidos = [], []
    estudo = (RAIZ_METODO / "templates" / "estudo-de-abordagem.md").read_text(encoding="utf-8")
    arquivos = {
        "AGENTS.md": agents_md(a.nome, a.linguagem),
        "CLAUDE.md": "@AGENTS.md\n",
        "docs/estudo-de-abordagem.md": estudo.replace("<projeto>", a.nome),
        "docs/adr/0001-registro-de-decisoes.md": ADR,
        ".github/workflows/ci.yml": ci_yml(a.linguagem),
        ".gitignore": GITIGNORE,
    }
    if a.linguagem == "python":
        # Sem nenhum teste o pytest sai com código 5 e a primeira CI nasce vermelha.
        arquivos["tests/test_fumaca.py"] = FUMACA_PY
    arquivos.update(ARQUIVOS_LINT.get(a.linguagem, {}))
    for rel, conteudo in arquivos.items():
        escrever(destino, rel, conteudo, criados, mantidos)
    if not (destino / ".git").exists():
        subprocess.run(["git", "init", "-q"], cwd=destino, check=True)
        criados.append(".git (git init)")
    print("Criados:", *(f"  {c}" for c in criados) or ["  nenhum"], sep="\n")
    if mantidos:
        print("Já existiam (não mexi):", *(f"  {m}" for m in mantidos), sep="\n")
    print("\nPróximo passo: preencha o AGENTS.md e rode o estudo de abordagem (/estudo).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
