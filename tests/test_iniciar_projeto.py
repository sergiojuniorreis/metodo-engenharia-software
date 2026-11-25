"""Testes do kit de início de projeto."""
import json
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

    def test_python_nasce_com_teste_de_fumaca(self):
        self.assertEqual(rodar(self.pasta, "--nome", "A", "--linguagem", "python").returncode, 0)
        self.assertTrue((self.pasta / "tests" / "test_fumaca.py").exists())
        self.assertIn("pytest==", (self.pasta / ".github/workflows/ci.yml").read_text(encoding="utf-8"))

    def test_outra_linguagem_avisa_sem_arquivo_do_projeto(self):
        pasta = Path(self._tmp.name) / "go"
        self.assertEqual(rodar(pasta, "--nome", "B", "--linguagem", "go").returncode, 0)
        ci = (pasta / ".github/workflows/ci.yml").read_text(encoding="utf-8")
        self.assertIn("if ls go.mod", ci)
        self.assertIn("::notice::", ci)

    def test_python_nasce_com_lint_antes_do_teste(self):
        self.assertEqual(rodar(self.pasta, "--nome", "A", "--linguagem", "python").returncode, 0)
        ruff = (self.pasta / "ruff.toml").read_text(encoding="utf-8")
        self.assertIn("[lint]", ruff)
        ci = (self.pasta / ".github/workflows/ci.yml").read_text(encoding="utf-8")
        self.assertIn("ruff==", ci)
        self.assertLess(ci.index("ruff check ."), ci.index("python -m pytest"))
        self.assertLess(ci.index("ruff format --check ."), ci.index("python -m pytest"))
        guia = (self.pasta / "docs/lint-e-formatacao.md").read_text(encoding="utf-8")
        self.assertIn("ruff==", guia)
        self.assertIn("Desfazer", guia)

    def test_typescript_nasce_com_eslint_e_prettier(self):
        self.assertEqual(rodar(self.pasta, "--nome", "T", "--linguagem", "typescript").returncode, 0)
        for rel in ["eslint.config.mjs", ".prettierrc.json", ".prettierignore", "docs/lint-e-formatacao.md"]:
            self.assertTrue((self.pasta / rel).exists(), rel)
        prettierrc = json.loads((self.pasta / ".prettierrc.json").read_text(encoding="utf-8"))
        self.assertEqual(prettierrc["endOfLine"], "auto")  # não reescreve o fim de linha do arquivo
        ci = (self.pasta / ".github/workflows/ci.yml").read_text(encoding="utf-8")
        self.assertLess(ci.index("npm run lint"), ci.index("npm test"))
        guia = (self.pasta / "docs/lint-e-formatacao.md").read_text(encoding="utf-8")
        self.assertIn("prettier@", guia)
        self.assertIn("eslint@", guia)

    def test_ci_e_yaml_valido_em_todas_as_linguagens(self):
        # Escalar simples com ": " no meio é mapeamento aninhado: o YAML não abre e a CI não roda.
        for ling in ["python", "typescript", "java", "go", "csharp", "rust", "outra"]:
            with self.subTest(ling=ling):
                pasta = Path(self._tmp.name) / f"yaml-{ling}"
                self.assertEqual(rodar(pasta, "--nome", "Y", "--linguagem", ling).returncode, 0)
                ci = (pasta / ".github/workflows/ci.yml").read_text(encoding="utf-8")
                for linha in ci.splitlines():
                    if linha.strip().startswith("- run: ") and linha.strip() != "- run: |":
                        valor = linha.strip()[len("- run: "):]
                        self.assertNotIn(": ", valor, linha)
                        self.assertNotIn(" #", valor, linha)

    def test_lint_so_onde_ha_config(self):
        pasta = Path(self._tmp.name) / "go"
        self.assertEqual(rodar(pasta, "--nome", "G", "--linguagem", "go").returncode, 0)
        self.assertFalse((pasta / "ruff.toml").exists())
        self.assertFalse((pasta / ".prettierrc.json").exists())
        self.assertFalse((pasta / "docs/lint-e-formatacao.md").exists())

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
