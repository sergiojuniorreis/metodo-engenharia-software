"""Testes do kit de início de projeto."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "iniciar_projeto.py"
ESPERADOS = ["AGENTS.md", "CLAUDE.md", "docs/estudo-de-abordagem.md",
             "docs/adr/0001-registro-de-decisoes.md", ".github/workflows/ci.yml", ".gitignore"]


def rodar(pasta, *args):
    return subprocess.run([sys.executable, "-I", str(SCRIPT), str(pasta), *args],
                          capture_output=True, text=True, encoding="utf-8", errors="replace")


class Kit(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.pasta = Path(self._tmp.name) / "novo"

    def tearDown(self):
        self._tmp.cleanup()

    def test_cria_a_estrutura(self):
        r = rodar(self.pasta, "--nome", "Agenda", "--linguagem", "python")
        self.assertEqual(r.returncode, 0, r.stderr)
        for rel in ESPERADOS:
            self.assertTrue((self.pasta / rel).exists(), rel)
        self.assertTrue((self.pasta / ".git").exists())
        agents = (self.pasta / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("# Agenda", agents)
        self.assertNotIn("<!--", agents)
        self.assertIn("python -m pytest", agents)
        self.assertEqual((self.pasta / "CLAUDE.md").read_text(encoding="utf-8"), "@AGENTS.md\n")

    def test_ci_por_linguagem(self):
        for ling, cmd in [("go", "go test ./..."), ("typescript", "npm test"), ("rust", "cargo test")]:
            with self.subTest(ling=ling):
                pasta = Path(self._tmp.name) / ling
                self.assertEqual(rodar(pasta, "--nome", "X", "--linguagem", ling).returncode, 0)
                ci = (pasta / ".github/workflows/ci.yml").read_text(encoding="utf-8")
                self.assertIn(cmd, ci)
                self.assertIn("gitleaks", ci)
                self.assertIn("fetch-depth: 0", ci)

    def test_nao_sobrescreve(self):
        self.pasta.mkdir(parents=True)
        (self.pasta / "AGENTS.md").write_text("meu conteúdo", encoding="utf-8")
        r = rodar(self.pasta, "--nome", "Agenda", "--linguagem", "python")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual((self.pasta / "AGENTS.md").read_text(encoding="utf-8"), "meu conteúdo")
        self.assertIn("Já existiam", r.stdout)

    def test_linguagem_invalida(self):
        r = rodar(self.pasta, "--nome", "X", "--linguagem", "cobol")
        self.assertNotEqual(r.returncode, 0)


if __name__ == "__main__":
    unittest.main()
