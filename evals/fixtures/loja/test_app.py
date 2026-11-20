import unittest

from app import gravar_pagamento, processar_pedido


class ApiFalsa:
    def __init__(self):
        self.chamadas = 0

    def cobrar(self, pedido_id, valor):
        self.chamadas += 1
        return {"id_cobranca": f"C-{pedido_id}"}


class TestLoja(unittest.TestCase):
    def test_total(self):
        cliente = {"nome": "Fulano de Teste", "cpf": "000.000.000-00", "email": "fulano@exemplo.test"}
        self.assertEqual(processar_pedido(cliente, [("P1", 2)]), 7000)

    def test_produto_inexistente(self):
        with self.assertRaises(ValueError):
            processar_pedido({}, [("X", 1)])

    def test_pagamento(self):
        api = ApiFalsa()
        self.assertEqual(gravar_pagamento(7, 7000, api), "C-7")
        self.assertEqual(api.chamadas, 1)


if __name__ == "__main__":
    unittest.main()
