import unittest

from loja import abrir_pedido, importar_pedidos
from notificacao import destinatarios
from pedidos import Pedido


class TestOcultoDefault(unittest.TestCase):
    def test_carrinhos_independentes(self):
        a = abrir_pedido("ana@ex.com")
        a.adicionar("caneca", 1, 3000)
        a.aplicar_cupom("PRIMEIRA")
        b = abrir_pedido("bia@ex.com")
        self.assertEqual(b.itens, [])
        self.assertEqual(len(b.cupons), 0)
        self.assertEqual(b.total_centavos(), 0)

    def test_pedido_criado_direto(self):
        a = Pedido("ana@ex.com")
        a.adicionar("caneca", 1, 3000)
        a.aplicar_cupom("X")
        b = Pedido("bia@ex.com")
        self.assertEqual(b.itens, [])
        self.assertEqual(len(b.cupons), 0)

    def test_importacao_nao_contamina(self):
        ps = importar_pedidos(["ana@ex.com;caneca;1;3000", "bia@ex.com;prato;2;1500",
                               "ana@ex.com;copo;3;500"])
        por = {p.cliente: p for p in ps}
        self.assertEqual(por["ana@ex.com"].itens, [("caneca", 1, 3000), ("copo", 3, 500)])
        self.assertEqual(por["bia@ex.com"].itens, [("prato", 2, 1500)])
        self.assertEqual(Pedido("caio@ex.com").itens, [])
        self.assertEqual(abrir_pedido("caio@ex.com").itens, [])

    def test_itens_explicitos_mantidos(self):
        p = Pedido("ana@ex.com", [("caneca", 1, 3000)], {"CUPOM"})
        self.assertEqual(p.itens, [("caneca", 1, 3000)])
        self.assertEqual(set(p.cupons), {"CUPOM"})

    def test_destinatarios_nao_acumulam(self):
        a = destinatarios(abrir_pedido("ana@ex.com"))
        b = destinatarios(abrir_pedido("bia@ex.com"))
        self.assertEqual(list(b), ["bia@ex.com"])
        self.assertEqual(list(a), ["ana@ex.com"])

    def test_destinatarios_com_copias(self):
        r = destinatarios(abrir_pedido("ana@ex.com"), ["vendas@loja.com"])
        self.assertEqual(sorted(r), ["ana@ex.com", "vendas@loja.com"])
        r2 = destinatarios(abrir_pedido("bia@ex.com"), ["vendas@loja.com"])
        self.assertEqual(sorted(r2), ["bia@ex.com", "vendas@loja.com"])


if __name__ == "__main__":
    unittest.main()
