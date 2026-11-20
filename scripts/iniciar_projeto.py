"""Kit de início de projeto: cria no repositório a estrutura que o método pressupõe.

Cria (sem sobrescrever o que já existe):
  AGENTS.md, CLAUDE.md                      camada quente do projeto (§18)
  docs/estudo-de-abordagem.md               §3, para preencher
  docs/adr/0001-registro-de-decisoes.md      primeiro ADR
  .github/workflows/ci.yml                  teste da linguagem + segredo no histórico
  .gitignore                                segredos e lixo comum
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
GITLEAKS = "gitleaks/gitleaks-action@ff98106e4c7b2bc287b24eaf42907196329070c7 # v2.3.9"
CHECKOUT = "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1"

TESTE = {
    "python": ["if [ -f requirements.txt ]; then python -m pip install -r requirements.txt; fi",
               "python -m pip install pytest", "python -m pytest"],
    "typescript": ["npm ci", "npm test"],
    "java": ["if [ -f mvnw ]; then ./mvnw -B verify; elif [ -f gradlew ]; then ./gradlew test; else mvn -B verify; fi"],
    "go": ["go vet ./...", "go test ./..."],
    "csharp": ["dotnet test"],
    "rust": ["cargo test"],
    "outra": ["echo 'Defina o comando de teste do projeto neste passo (§5, comando único)' && exit 1"],
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


def ci_yml(linguagem):
    passos = "\n".join(f"      - run: {cmd}" for cmd in TESTE[linguagem])
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
