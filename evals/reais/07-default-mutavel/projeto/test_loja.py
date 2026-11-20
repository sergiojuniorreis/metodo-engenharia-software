import unittest

from loja import abrir_pedido, importar_pedidos
from notificacao import destinatarios
from pedidos import Pedido


class TestLoja(unittest.TestCase):
    def test_total(self):
        p = Pedido("ana@ex.com", [("caneca", 2, 3000), ("prato", 1, 1500)])
        self.assertEqual(p.total_centavos(), 7500)

    def test_importar_agrupa_por_cliente(self):
        ps = importar_pedidos(["ana@ex.com;caneca;1;3000", "ana@ex.com;prato;2;1500"])
        self.assertEqual(len(ps), 1)

    def test_destinatarios_com_copia(self):
        p = abrir_pedido("ana@ex.com")
        self.assertIn("ana@ex.com", destinatarios(p, ["vendas@loja.com"]))


if __name__ == "__main__":
    unittest.main()
