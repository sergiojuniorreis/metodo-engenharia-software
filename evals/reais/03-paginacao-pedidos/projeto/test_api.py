import unittest

import api
import repositorio


class TestApi(unittest.TestCase):
    def test_sem_pedidos(self):
        conn = repositorio.conectar()
        r = api.listar_pedidos(conn)
        self.assertEqual(r["itens"], [])
        self.assertEqual(r["pagina"], 1)


if __name__ == "__main__":
    unittest.main()
