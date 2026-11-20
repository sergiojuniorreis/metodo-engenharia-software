import unittest

import admin
from catalogo import Catalogo, criar_banco


class TestOcultoCache(unittest.TestCase):
    def setUp(self):
        self.conn = criar_banco()
        self.cat = Catalogo(self.conn)
        self.a = self.cat.cadastrar("Cafeteira", "cozinha", 10000)
        self.b = self.cat.cadastrar("Liquidificador", "cozinha", 20000)
        self.c = self.cat.cadastrar("Furadeira", "ferramentas", 30000)
        for pid in (self.a, self.b, self.c):
            self.cat.obter_produto(pid)  # pagina de produto ja visitada: cache quente

    def _preco(self, pid):
        return self.cat.obter_produto(pid)["preco_centavos"]

    def test_painel_salvar_preco(self):
        self.assertEqual(admin.salvar_preco(self.cat, self.a, 12345)["preco_centavos"], 12345)
        self.assertEqual(self._preco(self.a), 12345)

    def test_atualizar_preco_direto(self):
        self.cat.atualizar_preco(self.b, 25000)
        self.assertEqual(self._preco(self.b), 25000)
        self.assertEqual(self._preco(self.a), 10000)

    def test_reajuste_em_massa(self):
        lista = admin.reajuste_em_massa(self.cat, "cozinha", 10)
        self.assertEqual([p["preco_centavos"] for p in lista], [11000, 22000])
        self.assertEqual(self._preco(self.a), 11000)
        self.assertEqual(self._preco(self.c), 30000)

    def test_reajuste_pelo_job(self):
        self.cat.reajustar_categoria("ferramentas", 5)
        self.assertEqual(self._preco(self.c), 31500)

    def test_cache_continua_evitando_banco(self):
        self.cat.atualizar_preco(self.a, 15000)
        self.cat.obter_produto(self.a)
        consultas = []
        self.conn.set_trace_callback(consultas.append)
        try:
            for _ in range(5):
                self.assertEqual(self._preco(self.a), 15000)
                self.assertEqual(self._preco(self.c), 30000)
        finally:
            self.conn.set_trace_callback(None)
        self.assertEqual(consultas, [], "leituras repetidas sem alteracao foram ao banco")


if __name__ == "__main__":
    unittest.main()
