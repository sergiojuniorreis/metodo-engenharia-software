import unittest

from checkout import finalizar
from estoque import Estoque


class TestEstoque(unittest.TestCase):
    def test_reserva_simples(self):
        e = Estoque({"A": 3})
        self.assertTrue(e.reservar("A", 2))
        self.assertFalse(e.reservar("A", 2))
        self.assertEqual(e.saldo("A"), 1)

    def test_checkout_tudo_ou_nada(self):
        e = Estoque({"A": 5, "B": 0})
        self.assertFalse(finalizar(e, {"A": 1, "B": 1}))
        self.assertEqual(e.saldo("A"), 5)


if __name__ == "__main__":
    unittest.main()
