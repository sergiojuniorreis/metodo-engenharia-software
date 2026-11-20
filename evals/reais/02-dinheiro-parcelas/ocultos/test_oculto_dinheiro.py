import unittest
from decimal import Decimal

from financeiro import aplicar_desconto, parcelar, total_pedido


def D(x):
    return Decimal(str(x))


class TestOcultoDinheiro(unittest.TestCase):
    def _confere(self, valor, n):
        ps = [D(p) for p in parcelar(valor, n)]
        self.assertEqual(len(ps), n)
        self.assertEqual(sum(ps), Decimal(valor), f"{valor} em {n}x: {ps}")
        self.assertLessEqual(max(ps) - min(ps), Decimal("0.01"))
        for p in ps:
            self.assertEqual(p, p.quantize(Decimal("0.01")), f"parcela com mais de 2 casas: {p}")
            self.assertGreater(p, 0)

    def test_parcelas_somam_o_total(self):
        for valor, n in [("100.00", 3), ("10.00", 3), ("200.00", 7), ("1000.00", 12),
                         ("0.05", 2), ("99.99", 4), ("90.00", 3)]:
            self._confere(valor, n)

    def test_desconto_arredonda_certo(self):
        self.assertEqual(D(aplicar_desconto("1.15", 10)), Decimal("1.04"))
        self.assertEqual(D(aplicar_desconto("1.30", 5)), Decimal("1.24"))
        self.assertEqual(D(aplicar_desconto("1.14", 25)), Decimal("0.86"))
        self.assertEqual(D(aplicar_desconto("200.00", 10)), Decimal("180.00"))

    def test_total_sem_regressao(self):
        self.assertEqual(D(total_pedido([("10.00", 2), ("5.50", 1)])), Decimal("25.50"))
        self.assertEqual(D(total_pedido([("0.10", 1)] * 3)), Decimal("0.30"))
        self.assertEqual(D(total_pedido([("1.10", 3), ("19.99", 7)])), Decimal("143.23"))


if __name__ == "__main__":
    unittest.main()
