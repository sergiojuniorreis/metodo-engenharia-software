"""Testes do validador: cada defeito plantado numa cópia do repositório tem de reprovar.

Uso: python -m unittest discover -s tests -v
"""
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
IGNORAR = shutil.ignore_patterns(".git", "docs", "__pycache__")


def rodar(raiz):
    r = subprocess.run(
        [sys.executable, "-I", str(raiz / "scripts" / "validar.py")],
        capture_output=True, text=True, encoding="utf-8",
    )
    return r.returncode, r.stdout


class Validador(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.raiz = Path(self._tmp.name) / "repo"
        shutil.copytree(RAIZ, self.raiz, ignore=IGNORAR)

    def tearDown(self):
        self._tmp.cleanup()

    def acrescentar(self, rel, texto):
        p = self.raiz / rel
        p.write_text(p.read_text(encoding="utf-8") + texto, encoding="utf-8")

    def trocar(self, rel, antigo, novo):
        p = self.raiz / rel
        t = p.read_text(encoding="utf-8")
        self.assertIn(antigo, t, f"pré-condição: '{antigo}' em {rel}")
        p.write_text(t.replace(antigo, novo, 1), encoding="utf-8")

    def reprova(self, trecho):
        codigo, saida = rodar(self.raiz)
        self.assertEqual(codigo, 1, saida)
        self.assertIn(trecho, saida)

    def test_repositorio_limpo_passa(self):
        codigo, saida = rodar(self.raiz)
        self.assertEqual(codigo, 0, saida)

    def test_secao_inexistente(self):
        self.acrescentar("references/15-vocabulario.md", "\nVer §99.\n")
        self.reprova("§99 não existe")

    def test_subsecao_inexistente(self):
        self.acrescentar("references/15-vocabulario.md", "\nVer §16.6.42.\n")
        self.reprova("§16.6.42 não existe")

    def test_item_da_pauta_inexistente(self):
        self.acrescentar("references/15-vocabulario.md", "\nPauta §14.6 item 99.\n")
        self.reprova("item 99 da pauta")

    def test_caminho_citado_inexistente(self):
        self.acrescentar("README.md", "\nLeia `references/nao-existe.md`.\n")
        self.reprova("caminho citado não existe")

    def test_link_quebrado(self):
        self.acrescentar("README.md", "\n[x](nao-existe.md)\n")
        self.reprova("link quebrado")

    def test_arquivo_de_referencia_sem_rota(self):
        (self.raiz / "references" / "orfao.md").write_text("# §99 — órfão\n", encoding="utf-8")
        self.reprova("não está na tabela 'Como carregar'")

    def test_rota_para_arquivo_inexistente(self):
        self.trocar("SKILL.md", "`14-portao.md` |", "`14-portao-x.md` |")
        self.reprova("14-portao-x.md, que não existe")

    def test_agente_sem_modelo(self):
        p = self.raiz / "agents" / "auditor-entrega.md"
        p.write_text(re.sub(r"^model: .*\n", "", p.read_text(encoding="utf-8"), flags=re.M), encoding="utf-8")
        self.reprova("model ausente ou desconhecido")

    def test_agente_com_nome_errado(self):
        self.trocar("agents/auditor-entrega.md", "name: auditor-entrega", "name: outro")
        self.reprova("diferente do arquivo")

    def test_agente_com_ferramenta_desconhecida(self):
        self.trocar("agents/especialista-seguranca.md", "tools: Read, Glob, Grep, Bash", "tools: Read, Hack")
        self.reprova("ferramentas desconhecidas")

    def test_padrao_de_segredo(self):
        self.acrescentar("agents/README.md", "\nchave ghp_" + "a" * 30 + "\n")
        self.reprova("padrão de segredo")

    def test_descricao_da_skill_longa_demais(self):
        self.trocar("SKILL.md", "description: ", "description: " + "x" * 1100)
        self.reprova("acima de 1024")


if __name__ == "__main__":
    unittest.main()
