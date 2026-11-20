import unittest

import admin
from catalogo import Catalogo, criar_banco


class TestCatalogo(unittest.TestCase):
    def setUp(self):
        self.cat = Catalogo(criar_banco())
        self.pid = self.cat.cadastrar("Cafeteira", "cozinha", 19990)

    def test_obter_produto(self):
        self.assertEqual(self.cat.obter_produto(self.pid)["preco_centavos"], 19990)
        self.assertIsNone(self.cat.obter_produto(999))

    def test_preco_invalido(self):
        with self.assertRaises(ValueError):
            admin.salvar_preco(self.cat, self.pid, 0)


if __name__ == "__main__":
    unittest.main()
