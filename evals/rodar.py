"""Roda os evals com e sem a skill e grava o resultado bruto de cada execução.

Dois conjuntos:
  reais       — cenários de erros reais escritos por um agente que NÃO leu o método. Cada um traz
                testes de aceitação OCULTOS: o agente avaliado não os vê; eles entram só depois que
                ele termina. Passa quem corrige no ponto certo sem quebrar o resto. (evals/reais/)
  heuristico  — cenários de comportamento conferidos por heurística de texto e arquivos
                (evals/cenarios.json, fixtures em evals/fixtures/).

Cada execução trabalha numa cópia temporária; nunca num projeto real. A ordem das execuções é
embaralhada (semente gravada) para que hora e cache não favoreçam um modo.

Uso:
  python -I evals/rodar.py --conjunto reais --repeticoes 3 --paralelo 4
  python -I evals/rodar.py --conjunto heuristico --cenario projeto-novo --modo com
  python -I evals/rodar.py --teto-usd 1.00        # teto de gasto por execução

Requer o Claude Code (`claude`) e a skill instalada em ~/.claude/skills/.
"""
import argparse
import concurrent.futures
import datetime
import hashlib
import json
import random
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
SKILL = Path.home() / ".claude" / "skills" / "metodo-engenharia-software"
IGNORAR = shutil.ignore_patterns("__pycache__", "*.pyc", ".git")
# Os mesmos comandos liberados nos dois shells, para que a escolha do shell pelo agente não vire
# vantagem de um modo sobre o outro.
_CMDS = ["python *", "py *", "git status*", "git diff*", "git log*"]
FERRAMENTAS_PERMITIDAS = ["Read", "Glob", "Grep", "Edit", "Write",
                          *[f"Bash({c})" for c in _CMDS], *[f"PowerShell({c})" for c in _CMDS]]
TEMPO_TESTES_S = 600


def sha256_pasta(pasta):
    h = hashlib.sha256()
    for p in sorted(pasta.rglob("*")):
        if p.is_file() and "__pycache__" not in p.parts:
            h.update(str(p.relative_to(pasta)).replace("\\", "/").encode())
            h.update(p.read_bytes())
    return h.hexdigest()[:16] if pasta.exists() else None


def hash_arquivo(p):
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None


def preparar(origem):
    pasta = Path(tempfile.mkdtemp(prefix="eval-")) / "projeto"
    shutil.copytree(origem, pasta, ignore=IGNORAR)
    for cmd in (["git", "init", "-q"], ["git", "add", "-A"],
                ["git", "-c", "user.name=eval", "-c", "user.email=eval@exemplo.test",
                 "-c", "core.autocrlf=false", "commit", "-q", "-m", "base", "--allow-empty"]):
        subprocess.run(cmd, cwd=pasta, check=True, capture_output=True)
    return pasta


def executar(prompt, pasta, modo, teto):
    cmd = [shutil.which("claude"), "-p", "--output-format", "stream-json", "--verbose",
           "--permission-mode", "acceptEdits", "--strict-mcp-config", "--no-session-persistence",
           "--max-budget-usd", f"{teto:.2f}", "--allowedTools", *FERRAMENTAS_PERMITIDAS]
    if modo == "sem":
        cmd += ["--disallowedTools", "Skill"]
    r = subprocess.run(cmd, input=prompt, cwd=pasta, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=1200)
    ferramentas, skill, final, modelo = [], False, {}, None
    for linha in r.stdout.splitlines():
        try:
            ev = json.loads(linha)
        except json.JSONDecodeError:
            continue
        if ev.get("type") == "system" and ev.get("model"):
            modelo = ev.get("model")
        elif ev.get("type") == "assistant":
            for c in ev.get("message", {}).get("content", []):
                if c.get("type") == "tool_use":
                    ferramentas.append(c.get("name"))
                    if c.get("name") == "Skill" and "metodo-engenharia" in json.dumps(c.get("input", {})):
                        skill = True
        elif ev.get("type") == "result":
            final = ev
    uso = final.get("usage", {})
    return {
        "resposta": final.get("result", ""),
        "skill_disparou": skill,
        "ferramentas": ferramentas,
        "modelo": modelo,
        "turnos": final.get("num_turns"),
        "custo_usd": final.get("total_cost_usd"),
        "tokens": {k: uso.get(k) for k in ("input_tokens", "output_tokens",
                                             "cache_read_input_tokens", "cache_creation_input_tokens")},
        "duracao_ms": final.get("duration_ms"),
        "erro": None if final else (r.stderr[-500:] or "sem evento final"),
    }


def rodar_testes(pasta):
    try:
        r = subprocess.run([sys.executable, "-I", "-B", "-m", "unittest", "discover", "-s", ".", "-p", "test*.py"],
                           cwd=pasta, capture_output=True, text=True, encoding="utf-8", errors="replace",
                           timeout=TEMPO_TESTES_S)
    except subprocess.TimeoutExpired:
        return False, f"tempo esgotado ({TEMPO_TESTES_S}s)"
    resumo = (r.stderr.strip().splitlines() or [""])[-1]
    return r.returncode == 0, resumo


# --- conjunto heurístico -------------------------------------------------------------------

def conferir(check, pasta, resposta, hashes_antes):
    t = check["tipo"]
    if t == "resposta_contem":
        return bool(re.search(check["regex"], resposta))
    if t == "resposta_nao_contem":
        return not re.search(check["regex"], resposta)
    if t == "arquivo_nao_contem":
        p = pasta / check["caminho"]
        return p.exists() and not re.search(check["regex"], p.read_text(encoding="utf-8"))
    if t == "arquivo_inalterado":
        return hash_arquivo(pasta / check["caminho"]) == hashes_antes.get(check["caminho"])
    if t == "nenhum_arquivo_contem":
        for p in pasta.rglob("*"):
            if p.is_file() and ".git" not in p.parts:
                try:
                    if re.search(check["regex"], p.read_text(encoding="utf-8")):
                        return False
                except UnicodeDecodeError:
                    continue
        return True
    if t == "sem_arquivos_novos":
        return not [p for p in pasta.rglob("*") if p.suffix in check["extensoes"] and ".git" not in p.parts]
    if t == "testes_passam":
        return rodar_testes(pasta)[0]
    if t == "log_sem_dado_pessoal":
        texto = (pasta / check["caminho"]).read_text(encoding="utf-8")
        for linha in texto.splitlines():
            if re.search(r"\b(log\.\w+|logging\.\w+|print)\(", linha):
                cita = any(re.search(rf"['\"]{c}['\"]|\.{c}\b", linha) for c in check["campos"])
                if cita and not re.search(r"(?i)mascar|ofusc|mask|anonim|hash", linha):
                    return False
        return True
    if t == "texto_ou_arquivos_contem":
        textos = [resposta]
        for p in pasta.rglob("*"):
            if p.is_file() and ".git" not in p.parts:
                try:
                    textos.append(p.read_text(encoding="utf-8"))
                except UnicodeDecodeError:
                    continue
        return bool(re.search(check["regex"], "\n".join(textos)))
    raise ValueError(f"tipo de verificação desconhecido: {t}")


def carregar(conjunto):
    if conjunto == "processo":
        cen = json.loads((AQUI / "processo.json").read_text(encoding="utf-8"))
        for c in cen:
            c["origem"] = AQUI / c["origem"]
            if c.get("ocultos"):
                c["ocultos"] = AQUI / c["ocultos"]
        return cen
    if conjunto == "heuristico":
        cen = json.loads((AQUI / "cenarios.json").read_text(encoding="utf-8"))
        for c in cen:
            c["origem"] = AQUI / "fixtures" / c["fixture"]
        return cen
    cen = []
    for d in sorted((AQUI / "reais").iterdir()):
        if (d / "cenario.json").exists():
            c = json.loads((d / "cenario.json").read_text(encoding="utf-8"))
            c["origem"], c["ocultos"] = d / "projeto", d / "ocultos"
            cen.append(c)
    return cen


def uma_execucao(c, modo, rep, conjunto, teto):
    pasta = preparar(c["origem"])
    try:
        antes = {str(p.relative_to(pasta)).replace("\\", "/"): hash_arquivo(p)
                 for p in pasta.rglob("*") if p.is_file() and ".git" not in p.parts}
        prompt = c.get("prompts", {}).get(modo) or c["prompt"]
        r = executar(prompt, pasta, modo, teto)
        r["checks"] = [{"descricao": ch["descricao"], "passou": conferir(ch, pasta, r["resposta"], antes),
                        "marcador": ch.get("marcador", False)}
                       for ch in c.get("checks", [])]
        if c.get("ocultos"):
            for oculto in c["ocultos"].glob("*.py"):
                shutil.copy(oculto, pasta / oculto.name)
            ok, resumo = rodar_testes(pasta)
            r["checks"].append({"descricao": "testes ocultos e visíveis passam", "passou": ok,
                                "resumo": resumo, "marcador": False})
        # Marcador do método (nível declarado, relatório) é registrado, mas não conta para passar:
        # o modo sem a skill não tem por que produzi-lo.
        r["passou"] = all(ch["passou"] for ch in r["checks"] if not ch["marcador"])
        r.update({"cenario": c["id"], "modo": modo, "repeticao": rep})
        return r
    finally:
        shutil.rmtree(pasta.parent, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conjunto", choices=["reais", "heuristico", "processo"], default="reais")
    ap.add_argument("--cenario")
    ap.add_argument("--modo", choices=["com", "sem"])
    ap.add_argument("--repeticoes", type=int, default=1)
    ap.add_argument("--paralelo", type=int, default=1)
    ap.add_argument("--teto-usd", type=float, default=1.00)
    ap.add_argument("--semente", type=int, default=None)
    a = ap.parse_args()
    cenarios = [c for c in carregar(a.conjunto) if not a.cenario or c["id"] == a.cenario]
    modos = [a.modo] if a.modo else ["com", "sem"]
    semente = a.semente if a.semente is not None else random.randrange(1 << 30)
    tarefas = [(c, m, r) for c in cenarios for m in modos for r in range(1, a.repeticoes + 1)]
    random.Random(semente).shuffle(tarefas)
    meta = {
        "data": datetime.datetime.now().isoformat(timespec="seconds"),
        "conjunto": a.conjunto, "repeticoes": a.repeticoes, "semente": semente, "teto_usd": a.teto_usd,
        "claude_code": subprocess.run([shutil.which("claude"), "--version"], capture_output=True,
                                      text=True).stdout.strip(),
        "hash_skill_instalada": sha256_pasta(SKILL),
    }
    resultados = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=a.paralelo) as ex:
        futuros = [ex.submit(uma_execucao, c, m, r, a.conjunto, a.teto_usd) for c, m, r in tarefas]
        for f in concurrent.futures.as_completed(futuros):
            r = f.result()
            resultados.append(r)
            print(f"{r['cenario']:28} {r['modo']:3} #{r['repeticao']} passou={r['passou']!s:5} "
                  f"skill={r['skill_disparou']!s:5} custo={r['custo_usd']}", flush=True)
    meta["modelos"] = sorted({r["modelo"] for r in resultados if r["modelo"]})
    saida = AQUI / "resultados" / f"{datetime.datetime.now():%Y-%m-%d-%H%M%S}-{a.conjunto}.json"
    saida.write_text(json.dumps({"meta": meta, "execucoes": resultados}, ensure_ascii=False, indent=2),
                     encoding="utf-8")
    print("\nResumo (passou / total):")
    for c in cenarios:
        linha = [f"{c['id']:28}"]
        for m in modos:
            rs = [r for r in resultados if r["cenario"] == c["id"] and r["modo"] == m]
            linha.append(f"{m}: {sum(r['passou'] for r in rs)}/{len(rs)}")
        print("  ".join(linha))
    print(f"\nresultado: {saida}")


if __name__ == "__main__":
    main()
