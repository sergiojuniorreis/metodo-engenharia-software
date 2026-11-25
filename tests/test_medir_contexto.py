"""Testes do medidor de contexto: o que cada cenário carrega, em caracteres, com o contrato do §14.4."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SCRIPT = RAIZ / "scripts" / "medir_contexto.py"


def rodar(*args):
    return subprocess.run([sys.executable, "-I", str(SCRIPT), *args],
                          capture_output=True, text=True, encoding="utf-8", errors="replace")


class Medidor(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.saida = self.tmp / "contexto.json"

    def tearDown(self):
        self._tmp.cleanup()

    def medir(self, *extra):
        r = rodar("--json", str(self.saida), *extra)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(len(r.stdout.strip().splitlines()), 1, r.stdout)  # uma linha na tela
        return json.loads(self.saida.read_text(encoding="utf-8"))

    def test_cenarios_crescem_em_ordem(self):
        d = self.medir()
        c = {s["cenario"]: s["caracteres"] for s in d["cenarios"]}
        self.assertLess(c["inicio"], c["trivial"])
        self.assertLess(c["trivial"], c["padrao"])

    def test_inicio_nao_carrega_o_nucleo(self):
        d = self.medir()
        inicio = next(s for s in d["cenarios"] if s["cenario"] == "inicio")
        self.assertNotIn("SKILL.md", inicio["arquivos"])
        self.assertIn("SKILL.md (description)", inicio["arquivos"])

    def test_trivial_nao_carrega_o_portao(self):
        d = self.medir()
        trivial = next(s for s in d["cenarios"] if s["cenario"] == "trivial")
        self.assertNotIn("references/14-portao.md", trivial["arquivos"])
        padrao = next(s for s in d["cenarios"] if s["cenario"] == "padrao")
        self.assertIn("references/14-portao.md", padrao["arquivos"])

    def test_arquivos_de_fora_entram_quando_informados(self):
        claude = self.tmp / "CLAUDE.md"
        claude.write_text("a" * 100, encoding="utf-8")
        perfil = self.tmp / "PERFIL.md"
        perfil.write_text("b" * 50, encoding="utf-8")
        sem = {s["cenario"]: s["caracteres"] for s in self.medir()["cenarios"]}
        com = {s["cenario"]: s["caracteres"]
               for s in self.medir("--claude-md", str(claude), "--perfil", str(perfil))["cenarios"]}
        self.assertEqual(com["inicio"] - sem["inicio"], 100)  # CLAUDE.md entra sempre
        self.assertEqual(com["trivial"] - sem["trivial"], 150)  # o PERFIL entra com a skill

    def test_arquivo_de_fora_inexistente_e_saida_2(self):
        r = rodar("--json", str(self.saida), "--perfil", str(self.tmp / "nao-existe.md"))
        self.assertEqual(r.returncode, 2)


if __name__ == "__main__":
    unittest.main()
