"""Mede o que o método põe no contexto, por cenário, em caracteres (§18, "Medir").

Cenários:
  inicio   toda sessão, sem a skill disparar: descrição da skill, descrições dos comandos e o
           CLAUDE.md global (se informado)
  trivial  a skill disparou numa mudança trivial: + SKILL.md inteiro e o PERFIL.md (se informado)
  padrao   mudança de nível padrão: + references/14-portao.md

Conta caracteres, não tokens: o número de tokens depende do tokenizador e não é medido aqui.

Uso:
  python -I scripts/medir_contexto.py [--claude-md CAMINHO] [--perfil CAMINHO] [--json SAIDA]
Saída: uma linha na tela e o JSON em SAIDA. Código 0 medido; 2 arquivo informado não existe.
"""
import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def descricao(p):
    m = re.search(r"^description:\s*(.*)$", p.read_text(encoding="utf-8"), flags=re.M)
    return m.group(1) if m else ""


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--claude-md", type=Path)
    ap.add_argument("--perfil", type=Path)
    ap.add_argument("--json", type=Path, default=Path(tempfile.gettempdir()) / "medir_contexto.json")
    a = ap.parse_args(argv)
    for p in (a.claude_md, a.perfil):
        if p is not None and not p.is_file():
            print(f"não medido: {p} não existe", file=sys.stderr)
            return 2

    inicio = {"SKILL.md (description)": len(descricao(RAIZ / "SKILL.md"))}
    for c in sorted((RAIZ / "commands").glob("*.md")):
        inicio[f"commands/{c.name} (description)"] = len(descricao(c))
    if a.claude_md:
        inicio["CLAUDE.md"] = len(a.claude_md.read_text(encoding="utf-8"))
    trivial = dict(inicio, **{"SKILL.md": len((RAIZ / "SKILL.md").read_text(encoding="utf-8"))})
    if a.perfil:
        trivial["PERFIL.md"] = len(a.perfil.read_text(encoding="utf-8"))
    portao = "references/14-portao.md"
    padrao = dict(trivial, **{portao: len((RAIZ / portao).read_text(encoding="utf-8"))})

    cenarios = [{"cenario": nome, "caracteres": sum(arqs.values()), "arquivos": arqs}
                for nome, arqs in (("inicio", inicio), ("trivial", trivial), ("padrao", padrao))]
    resultado = {"unidade": "caracteres (não tokens)", "cenarios": cenarios}
    a.json.parent.mkdir(parents=True, exist_ok=True)
    a.json.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
    resumo = " · ".join(f"{c['cenario']} {c['caracteres']}" for c in cenarios)
    print(f"contexto (caracteres): {resumo} → {a.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
