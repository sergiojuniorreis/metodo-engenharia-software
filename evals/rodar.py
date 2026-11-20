"""Roda os cenários de evals com e sem a skill e grava o resultado.

Cada execução trabalha numa cópia temporária do projeto fictício (evals/fixtures), nunca num
projeto real. Mede: comportamento (verificações de cenarios.json), se a skill disparou sozinha,
tokens, custo e turnos.

Uso:
  python -I evals/rodar.py                      # todos os cenários, com e sem a skill
  python -I evals/rodar.py --cenario correcao-trivial --modo com
  python -I evals/rodar.py --teto-usd 1.00      # teto de gasto por execução (padrão 1.00)

Requer o Claude Code (comando `claude`) e a skill instalada em ~/.claude/skills.
"""
import argparse
import datetime
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
FERRAMENTAS_PERMITIDAS = ["Read", "Glob", "Grep", "Edit", "Write",
                          "Bash(python -m unittest*)", "Bash(git status*)", "Bash(git diff*)"]


def hash_arquivo(p):
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None


def preparar(fixture):
    pasta = Path(tempfile.mkdtemp(prefix="eval-")) / "projeto"
    shutil.copytree(AQUI / "fixtures" / fixture, pasta)
    for cmd in (["git", "init", "-q"], ["git", "add", "-A"],
                ["git", "-c", "user.name=eval", "-c", "user.email=eval@exemplo.test",
                 "commit", "-q", "-m", "base", "--allow-empty"]):
        subprocess.run(cmd, cwd=pasta, check=True)
    return pasta


def executar(prompt, pasta, modo, teto):
    cmd = [shutil.which("claude"), "-p", "--output-format", "stream-json", "--verbose",
           "--permission-mode", "acceptEdits", "--strict-mcp-config", "--no-session-persistence",
           "--max-budget-usd", f"{teto:.2f}", "--allowedTools", *FERRAMENTAS_PERMITIDAS]
    if modo == "sem":
        cmd += ["--disallowedTools", "Skill"]
    r = subprocess.run(cmd, input=prompt, cwd=pasta, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=900)
    ferramentas, skill, final = [], False, {}
    for linha in r.stdout.splitlines():
        try:
            ev = json.loads(linha)
        except json.JSONDecodeError:
            continue
        if ev.get("type") == "assistant":
            for c in ev.get("message", {}).get("content", []):
                if c.get("type") == "tool_use":
                    ferramentas.append(c.get("name"))
                    if c.get("name") == "Skill" and "metodo-engenharia" in json.dumps(c.get("input", {})):
                        skill = True
        elif ev.get("type") == "result":
            final = ev
    uso = final.get("usage", {})
    return {
        "codigo_saida": r.returncode,
        "resposta": final.get("result", ""),
        "skill_disparou": skill,
        "ferramentas": ferramentas,
        "turnos": final.get("num_turns"),
        "custo_usd": final.get("total_cost_usd"),
        "tokens": {k: uso.get(k) for k in ("input_tokens", "output_tokens",
                                             "cache_read_input_tokens", "cache_creation_input_tokens")},
        "duracao_ms": final.get("duration_ms"),
        "erro": None if final else (r.stderr[-500:] or "sem evento final"),
    }


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
        r = subprocess.run([sys.executable, "-I", "-m", "unittest", "-q"], cwd=pasta, capture_output=True)
        return r.returncode == 0
    if t == "log_sem_dado_pessoal":
        texto = (pasta / check["caminho"]).read_text(encoding="utf-8")
        for linha in texto.splitlines():
            if re.search(r"\b(log\.\w+|logging\.\w+|print)\(", linha):
                cita = any(re.search(rf"['\"]{c}['\"]|\.{c}\b", linha) for c in check["campos"])
                if cita and not re.search(r"(?i)mascar|ofusc|mask|anonim|hash", linha):
                    return False
        return True
    raise ValueError(f"tipo de verificação desconhecido: {t}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cenario")
    ap.add_argument("--modo", choices=["com", "sem"])
    ap.add_argument("--teto-usd", type=float, default=1.00)
    a = ap.parse_args()
    cenarios = json.loads((AQUI / "cenarios.json").read_text(encoding="utf-8"))
    if a.cenario:
        cenarios = [c for c in cenarios if c["id"] == a.cenario]
    modos = [a.modo] if a.modo else ["com", "sem"]
    resultados = []
    for c in cenarios:
        for modo in modos:
            pasta = preparar(c["fixture"])
            antes = {str(p.relative_to(pasta)).replace("\\", "/"): hash_arquivo(p)
                     for p in pasta.rglob("*") if p.is_file() and ".git" not in p.parts}
            r = executar(c["prompt"], pasta, modo, a.teto_usd)
            r["checks"] = [{"descricao": ch["descricao"], "passou": conferir(ch, pasta, r["resposta"], antes)}
                           for ch in c["checks"]]
            r["passou"] = all(ch["passou"] for ch in r["checks"])
            r.update({"cenario": c["id"], "modo": modo})
            resultados.append(r)
            print(f"{c['id']:18} {modo:3} passou={r['passou']!s:5} skill={r['skill_disparou']!s:5} "
                  f"custo={r['custo_usd']} turnos={r['turnos']}", flush=True)
            shutil.rmtree(pasta.parent, ignore_errors=True)
    data = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
    saida = AQUI / "resultados" / f"{data}.json"
    saida.write_text(json.dumps(resultados, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"resultado: {saida}")


if __name__ == "__main__":
    main()
