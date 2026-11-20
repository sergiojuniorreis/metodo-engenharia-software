import unittest

import api
import exportacao
import repositorio


def _banco(n):
    conn = repositorio.conectar()
    for i in range(1, n + 1):
        repositorio.inserir(conn, f"cliente{i}", f"{i}.00")
    return conn


def _ids(resp):
    return [item["id"] for item in resp["itens"]]


class TestOcultoPaginacao(unittest.TestCase):
    def test_primeira_pagina_tem_os_mais_antigos(self):
        conn = _banco(25)
        self.assertEqual(_ids(api.listar_pedidos(conn, 1)), list(range(1, 11)))
        self.assertEqual(_ids(api.listar_pedidos(conn)), list(range(1, 11)))

    def test_ultima_pagina_parcial(self):
        conn = _banco(25)
        self.assertEqual(_ids(api.listar_pedidos(conn, 2)), list(range(11, 21)))
        self.assertEqual(_ids(api.listar_pedidos(conn, 3)), list(range(21, 26)))
        self.assertEqual(_ids(api.listar_pedidos(conn, 4)), [])

    def test_total_de_paginas(self):
        self.assertEqual(api.listar_pedidos(_banco(25), 1)["total_paginas"], 3)
        self.assertEqual(api.listar_pedidos(_banco(20), 1)["total_paginas"], 2)
        self.assertEqual(api.listar_pedidos(_banco(1), 1)["total_paginas"], 1)

    def test_todas_as_paginas_cobrem_tudo_sem_repetir(self):
        conn = _banco(37)
        r = api.listar_pedidos(conn, 1)
        vistos = []
        for p in range(1, r["total_paginas"] + 1):
            vistos += _ids(api.listar_pedidos(conn, p))
        self.assertEqual(vistos, list(range(1, 38)))

    def test_exportacao_sem_duplicar_nem_perder(self):
        conn = _banco(250)
        linhas = exportacao.exportar_csv(conn).split("\n")
        self.assertEqual(linhas[0], "id;cliente;total")
        ids = [int(l.split(";")[0]) for l in linhas[1:]]
        self.assertEqual(ids, list(range(1, 251)))

    def test_exportacao_pequena(self):
        conn = _banco(7)
        ids = [int(l.split(";")[0]) for l in exportacao.exportar_csv(conn).split("\n")[1:]]
        self.assertEqual(ids, list(range(1, 8)))


if __name__ == "__main__":
    unittest.main()
