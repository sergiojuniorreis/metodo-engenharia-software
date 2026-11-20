import unittest

import clientes


class TestClientes(unittest.TestCase):
    def setUp(self):
        self.conn = clientes.criar_banco()
        clientes.cadastrar(self.conn, "Ana Silva", "Campinas")
        clientes.cadastrar(self.conn, "Bruno Silva", "Santos")
        clientes.cadastrar(self.conn, "Carla Souza", "Campinas")

    def test_busca_por_nome(self):
        nomes = [r[1] for r in clientes.buscar_por_nome(self.conn, "Silva")]
        self.assertEqual(nomes, ["Ana Silva", "Bruno Silva"])

    def test_busca_por_cidade(self):
        nomes = [r[1] for r in clientes.buscar_por_cidade(self.conn, "Campinas")]
        self.assertEqual(nomes, ["Ana Silva", "Carla Souza"])


if __name__ == "__main__":
    unittest.main()
