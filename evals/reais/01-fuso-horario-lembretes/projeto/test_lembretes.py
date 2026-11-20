import unittest
from datetime import datetime, timezone

from fusos import para_local
from lembretes import texto_lembrete


class TestLembretes(unittest.TestCase):
    def test_para_local_sao_paulo(self):
        m = datetime(2026, 5, 10, 15, 0, tzinfo=timezone.utc)
        self.assertEqual(para_local(m, "America/Sao_Paulo"), datetime(2026, 5, 10, 12, 0))

    def test_texto(self):
        m = datetime(2026, 5, 10, 15, 30, tzinfo=timezone.utc)
        self.assertEqual(texto_lembrete(m, "America/Sao_Paulo", "Consulta"), "Consulta - 10/05/2026 12:30")


if __name__ == "__main__":
    unittest.main()
