import unittest
from unittest import mock

import pagamentos
from gateway import GatewaySimulado


class _LoopSemFim(BaseException):
    pass


class GatewayLimitado(GatewaySimulado):
    """Interrompe o teste se o codigo insistir indefinidamente."""

    def cobrar(self, valor_centavos, chave_idempotencia=None):
        if self.chamadas >= 50:
            raise _LoopSemFim()
        return super().cobrar(valor_centavos, chave_idempotencia)


class TestOcultoCobranca(unittest.TestCase):
    def setUp(self):
        p = mock.patch("time.sleep", return_value=None)
        p.start()
        self.addCleanup(p.stop)
        self.conn = pagamentos.criar_banco()

    def _cobrar(self, pid, gw):
        try:
            return pagamentos.cobrar_pedido(self.conn, pid, gw)
        except _LoopSemFim:
            self.fail("cobrar_pedido insistiu sem limite")
        except Exception:
            return False

    def test_timeout_antes_de_cobrar_tenta_de_novo(self):
        pid = pagamentos.criar_pedido(self.conn, 1000)
        gw = GatewayLimitado(timeouts_antes=2)
        self._cobrar(pid, gw)
        self.assertEqual(pagamentos.status(self.conn, pid), "pago")
        self.assertEqual(len(gw.cobrancas), 1)

    def test_timeout_depois_de_cobrar_nao_cobra_duas_vezes(self):
        pid = pagamentos.criar_pedido(self.conn, 1000)
        gw = GatewayLimitado(timeouts_depois=1)
        self._cobrar(pid, gw)
        self.assertEqual(pagamentos.status(self.conn, pid), "pago")
        self.assertEqual(len(gw.cobrancas), 1, gw.cobrancas)

    def test_gateway_fora_do_ar_nao_fica_em_loop(self):
        pid = pagamentos.criar_pedido(self.conn, 1000)
        gw = GatewayLimitado(timeouts_antes=10 ** 6)
        self._cobrar(pid, gw)
        self.assertNotEqual(pagamentos.status(self.conn, pid), "pago")
        self.assertEqual(gw.cobrancas, [])

    def test_reprocessar_pelo_painel_depois_de_timeout_nao_duplica(self):
        pid = pagamentos.criar_pedido(self.conn, 1000)
        gw = GatewayLimitado(timeouts_depois=10 ** 6)  # cobrou, mas nenhuma resposta chega
        self._cobrar(pid, gw)
        self.assertNotEqual(pagamentos.status(self.conn, pid), "pago")
        gw.timeouts_depois = 0
        gw.chamadas = 0
        self._cobrar(pid, gw)  # operador reprocessa o pendente
        self.assertEqual(pagamentos.status(self.conn, pid), "pago")
        self.assertEqual(len(gw.cobrancas), 1, gw.cobrancas)

    def test_pedido_ja_pago_nao_e_cobrado_de_novo(self):
        pid = pagamentos.criar_pedido(self.conn, 1000)
        gw = GatewayLimitado()
        self._cobrar(pid, gw)
        self._cobrar(pid, gw)
        self.assertEqual(pagamentos.status(self.conn, pid), "pago")
        self.assertEqual(len(gw.cobrancas), 1)

    def test_pedidos_diferentes_sao_cobrados_separadamente(self):
        gw = GatewayLimitado()
        a = pagamentos.criar_pedido(self.conn, 1000)
        b = pagamentos.criar_pedido(self.conn, 2500)
        self._cobrar(a, gw)
        self._cobrar(b, gw)
        self.assertEqual(sorted(v for _, v in gw.cobrancas), [1000, 2500])
        self.assertEqual(pagamentos.status(self.conn, a), "pago")
        self.assertEqual(pagamentos.status(self.conn, b), "pago")


if __name__ == "__main__":
    unittest.main()
