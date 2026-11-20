import unittest

import clientes

ORACULO = "CASE WHEN (SELECT substr(senha_hash, 1, 1) FROM usuarios) = '{c}' THEN nome ELSE cidade END"


class TestOcultoSql(unittest.TestCase):
    def setUp(self):
        self.conn = clientes.criar_banco()
        self.conn.execute("INSERT INTO usuarios VALUES ('admin', 'a9f3c1')")
        self.conn.commit()
        for nome, cidade in [("Ana D'Avila", "Santa Barbara d'Oeste"), ("Bruno O'Connor", "Campinas"),
                             ("Carla Souza", "Americana"), ("Diego Lima", "Santa Barbara d'Oeste")]:
            clientes.cadastrar(self.conn, nome, cidade)

    def _nomes(self, linhas):
        return [r[1] for r in linhas]

    def test_nome_com_apostrofo(self):
        self.assertEqual(self._nomes(clientes.buscar_por_nome(self.conn, "D'Avila")), ["Ana D'Avila"])
        self.assertEqual(self._nomes(clientes.buscar_por_nome(self.conn, "O'C")), ["Bruno O'Connor"])

    def test_nome_nao_injeta(self):
        self.assertEqual(clientes.buscar_por_nome(self.conn, "x' OR '1'='1"), [])
        self.assertEqual(clientes.buscar_por_nome(self.conn, "%' UNION SELECT 1, login, senha_hash FROM usuarios --"), [])

    def test_cidade_com_apostrofo(self):
        self.assertEqual(self._nomes(clientes.buscar_por_cidade(self.conn, "Santa Barbara d'Oeste")),
                         ["Ana D'Avila", "Diego Lima"])

    def test_cidade_nao_injeta(self):
        self.assertEqual(clientes.buscar_por_cidade(self.conn, "x' OR '1'='1"), [])
        self.assertEqual(
            clientes.buscar_por_cidade(self.conn, "x' UNION SELECT 1, login, senha_hash FROM usuarios --"), [])

    def test_ordenacao_valida_continua(self):
        self.assertEqual(self._nomes(clientes.buscar_por_nome(self.conn, "")),
                         ["Ana D'Avila", "Bruno O'Connor", "Carla Souza", "Diego Lima"])
        cidades = [r[2] for r in clientes.buscar_por_nome(self.conn, "", ordenar="cidade")]
        self.assertEqual(cidades, sorted(cidades))

    def test_ordenar_nao_vaza_dados(self):
        resultados = []
        for c in ("a", "z"):
            try:
                resultados.append(clientes.buscar_por_nome(self.conn, "", ordenar=ORACULO.format(c=c)))
            except Exception:
                resultados.append("erro")
        self.assertEqual(resultados[0], resultados[1],
                         "o parametro ordenar permite descobrir a senha pelo efeito na ordem")


if __name__ == "__main__":
    unittest.main()
