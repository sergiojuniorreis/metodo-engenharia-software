import unittest

import pagamentos
from gateway import GatewaySimulado


class TestPagamentos(unittest.TestCase):
    def test_cobranca_normal(self):
        conn = pagamentos.criar_banco()
        pid = pagamentos.criar_pedido(conn, 5000)
        gw = GatewaySimulado()
        self.assertTrue(pagamentos.cobrar_pedido(conn, pid, gw))
        self.assertEqual(pagamentos.status(conn, pid), "pago")
        self.assertEqual(gw.cobrancas, [("tx1", 5000)])


if __name__ == "__main__":
    unittest.main()
