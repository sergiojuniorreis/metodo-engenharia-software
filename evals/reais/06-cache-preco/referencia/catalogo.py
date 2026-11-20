import sqlite3


def criar_banco():
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE produtos (id INTEGER PRIMARY KEY, nome TEXT, categoria TEXT, preco_centavos INTEGER)"
    )
    return conn


class Catalogo:
    """Leitura de produtos com cache em memoria: a pagina de produto e a mais acessada
    da loja e nao pode ir ao banco a cada visualizacao."""

    def __init__(self, conn):
        self.conn = conn
        self._cache = {}

    def cadastrar(self, nome, categoria, preco_centavos):
        cur = self.conn.execute(
            "INSERT INTO produtos (nome, categoria, preco_centavos) VALUES (?, ?, ?)",
            (nome, categoria, preco_centavos),
        )
        self.conn.commit()
        return cur.lastrowid

    def obter_produto(self, produto_id):
        if produto_id in self._cache:
            return dict(self._cache[produto_id])
        linha = self.conn.execute(
            "SELECT id, nome, categoria, preco_centavos FROM produtos WHERE id = ?", (produto_id,)
        ).fetchone()
        if linha is None:
            return None
        produto = {"id": linha[0], "nome": linha[1], "categoria": linha[2], "preco_centavos": linha[3]}
        self._cache[produto_id] = produto
        return dict(produto)

    def listar_categoria(self, categoria):
        ids = [r[0] for r in self.conn.execute(
            "SELECT id FROM produtos WHERE categoria = ? ORDER BY id", (categoria,))]
        return [self.obter_produto(i) for i in ids]

    def atualizar_preco(self, produto_id, preco_centavos):
        self.conn.execute("UPDATE produtos SET preco_centavos = ? WHERE id = ?", (preco_centavos, produto_id))
        self.conn.commit()
        self._cache.pop(produto_id, None)

    def reajustar_categoria(self, categoria, percentual):
        """Reajuste em massa (ex.: +8 para 8%), usado pela tela de reajuste e pelo job mensal."""
        self.conn.execute(
            "UPDATE produtos SET preco_centavos = CAST(ROUND(preco_centavos * (100 + ?) / 100.0) AS INTEGER)"
            " WHERE categoria = ?",
            (percentual, categoria),
        )
        self.conn.commit()
        for pid in [pid for pid, p in self._cache.items() if p["categoria"] == categoria]:
            del self._cache[pid]
