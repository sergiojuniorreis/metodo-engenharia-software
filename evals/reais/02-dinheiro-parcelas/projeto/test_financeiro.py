import unittest

from financeiro import aplicar_desconto, parcelar, total_pedido


class TestFinanceiro(unittest.TestCase):
    def test_total(self):
        self.assertEqual(total_pedido([("10.00", 2), ("5.50", 1)]), 25.5)

    def test_desconto(self):
        self.assertEqual(aplicar_desconto("200.00", 10), 180.0)

    def test_parcelas_exatas(self):
        self.assertEqual(parcelar("90.00", 3), [30.0, 30.0, 30.0])


if __name__ == "__main__":
    unittest.main()
