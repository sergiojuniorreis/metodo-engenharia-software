"""Valida o repositório do método: referências §, caminhos citados, agentes e segredos.

Uso: python scripts/validar.py   (código de saída 0 = tudo certo; 1 = falhas listadas)
Só biblioteca padrão. Roda igual local e na CI.
"""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FERRAMENTAS = {"Read", "Glob", "Grep", "Bash", "Edit", "Write", "WebSearch", "WebFetch", "NotebookEdit"}
PADROES_SEGREDO = [
    r"sk-[A-Za-z0-9_-]{20,}", r"ghp_[A-Za-z0-9]{20,}", r"github_pat_[A-Za-z0-9_]{20,}",
    r"AKIA[A-Z0-9]{16}", r"AIza[A-Za-z0-9_-]{30,}", r"xox[bp]-[A-Za-z0-9-]{10,}",
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----", r"eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}",
]
IGNORAR = {"docs", ".git", "node_modules"}

falhas = []
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def arquivos(sufixos):
    for p in sorted(RAIZ.rglob("*")):
        if p.is_file() and p.suffix in sufixos and not IGNORAR.intersection(p.relative_to(RAIZ).parts):
            yield p


def ler(p):
    return p.read_text(encoding="utf-8")


def secoes_definidas():
    """Seções que existem, tiradas dos próprios títulos."""
    definidas = set()
    for p in arquivos({".md"}):
        for linha in ler(p).splitlines():
            m = re.match(r"#{1,3} §(\d+(?:\.\d+)?)\b", linha)
            if m:
                definidas.add(m.group(1))
            m = re.match(r"## (\d+(?:\.\d+)?)\.?\s", linha)
            if m:
                definidas.add(m.group(1))
            if p.name.startswith("03-"):
                m = re.match(r"### ([A-D])\. ", linha)
                if m:
                    definidas.add("3" + m.group(1))
    # "§16" e "§17" sem subitem apontam para o conjunto de módulos/especialidades
    for grupo in ("16", "17"):
        if any(s.startswith(grupo + ".") for s in definidas):
            definidas.add(grupo)
    return definidas


def checar_referencias():
    definidas = secoes_definidas()
    for p in arquivos({".md"}):
        for n, linha in enumerate(ler(p).splitlines(), 1):
            for ref in re.findall(r"§(\d+(?:\.\d+)?[A-Z]?)", linha):
                if ref not in definidas:
                    falhas.append(f"{p.relative_to(RAIZ)}:{n}: §{ref} não existe")


def checar_caminhos():
    for p in arquivos({".md"}):
        for n, linha in enumerate(ler(p).splitlines(), 1):
            for cam in re.findall(r"`((?:references|agents|templates|scripts)/[^`*<>\s]+\.(?:md|py|ya?ml))`", linha):
                if not (RAIZ / cam).exists():
                    falhas.append(f"{p.relative_to(RAIZ)}:{n}: caminho citado não existe: {cam}")
            for cam in re.findall(r"\]\(([^)#:]+)\)", linha):
                if not (p.parent / cam).exists():
                    falhas.append(f"{p.relative_to(RAIZ)}:{n}: link quebrado: {cam}")


def cabecalho(p):
    texto = ler(p)
    if not texto.startswith("---\n"):
        return None
    fim = texto.find("\n---", 4)
    campos = {}
    for linha in texto[4:fim].splitlines():
        if ":" in linha:
            chave, valor = linha.split(":", 1)
            campos[chave.strip()] = valor.strip()
    return campos


def checar_agentes():
    for p in sorted((RAIZ / "agents").glob("*.md")):
        if p.name == "README.md":
            continue
        c = cabecalho(p)
        rel = p.relative_to(RAIZ)
        if c is None:
            falhas.append(f"{rel}: sem cabeçalho ---")
            continue
        if c.get("name") != p.stem:
            falhas.append(f"{rel}: name '{c.get('name')}' diferente do arquivo")
        if len(c.get("description", "")) < 40:
            falhas.append(f"{rel}: description ausente ou curta demais")
        desconhecidas = {t.strip() for t in c.get("tools", "").split(",")} - FERRAMENTAS
        if desconhecidas:
            falhas.append(f"{rel}: ferramentas desconhecidas: {sorted(desconhecidas)}")
        if f"`{p.stem}`" not in ler(RAIZ / "agents" / "README.md"):
            falhas.append(f"{rel}: agente não listado em agents/README.md")
    c = cabecalho(RAIZ / "SKILL.md") or {}
    if c.get("name") != "metodo-engenharia-software":
        falhas.append("SKILL.md: name ausente ou errado")
    if not 0 < len(c.get("description", "")) <= 1024:
        falhas.append("SKILL.md: description vazia ou acima de 1024 caracteres")


def checar_segredos():
    regex = re.compile("|".join(PADROES_SEGREDO))
    for p in arquivos({".md", ".py", ".yml", ".yaml", ".json", ".txt"}):
        if p.name == "validar.py":
            continue
        for n, linha in enumerate(ler(p).splitlines(), 1):
            if regex.search(linha):
                falhas.append(f"{p.relative_to(RAIZ)}:{n}: padrão de segredo (valor não impresso)")


checar_referencias()
checar_caminhos()
checar_agentes()
checar_segredos()

if falhas:
    print("\n".join(falhas))
    print(f"\n{len(falhas)} falha(s).")
    sys.exit(1)
print("ok: referências, caminhos, agentes e varredura de segredo")
