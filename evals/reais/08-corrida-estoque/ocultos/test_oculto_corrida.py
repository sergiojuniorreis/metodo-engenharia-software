import threading
import unittest

from checkout import finalizar
from estoque import Estoque


def _em_paralelo(funcoes):
    barreira = threading.Barrier(len(funcoes))
    resultados = [None] * len(funcoes)

    def rodar(i, f):
        barreira.wait()
        resultados[i] = f()

    ts = [threading.Thread(target=rodar, args=(i, f)) for i, f in enumerate(funcoes)]
    for t in ts:
        t.start()
    for t in ts:
        t.join(30)
    return resultados


class TestOcultoCorrida(unittest.TestCase):
    def test_nao_vende_mais_que_o_estoque(self):
        e = Estoque({"A": 10})
        r = _em_paralelo([lambda: e.reservar("A", 1)] * 50)
        self.assertEqual(r.count(True), 10)
        self.assertEqual(e.saldo("A"), 0)

    def test_reservas_e_devolucoes_simultaneas_nao_perdem_atualizacao(self):
        e = Estoque({"A": 100})
        fs = [lambda: e.reservar("A", 1)] * 40 + [lambda: e.devolver("A", 1)] * 40
        r = _em_paralelo(fs)
        self.assertEqual(r[:40].count(True), 40)
        self.assertEqual(e.saldo("A"), 100)

    def test_checkout_simultaneo(self):
        e = Estoque({"A": 5, "B": 5})
        r = _em_paralelo([lambda: finalizar(e, {"A": 1, "B": 1})] * 20)
        self.assertEqual(r.count(True), 5)
        self.assertEqual((e.saldo("A"), e.saldo("B")), (0, 0))

    def test_comportamento_sequencial_mantido(self):
        e = Estoque({"A": 2})
        self.assertFalse(e.reservar("A", 0))
        self.assertFalse(e.reservar("B", 1))
        self.assertTrue(e.reservar("A", 2))
        e.devolver("A", 1)
        self.assertEqual(e.saldo("A"), 1)
        self.assertEqual(len(e.auditoria), 2)


if __name__ == "__main__":
    unittest.main()
