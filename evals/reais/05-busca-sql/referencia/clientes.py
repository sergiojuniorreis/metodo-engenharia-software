import sqlite3

COLUNAS_ORDENAVEIS = {"nome": "nome", "cidade": "cidade"}


def criar_banco():
    conn = sqlite3.connect(":memory:")
    conn.executescript(
        """
        CREATE TABLE clientes (id INTEGER PRIMARY KEY, nome TEXT, cidade TEXT);
        CREATE TABLE usuarios (login TEXT, senha_hash TEXT);
        """
    )
    return conn


def cadastrar(conn, nome, cidade):
    conn.execute("INSERT INTO clientes (nome, cidade) VALUES (?, ?)", (nome, cidade))
    conn.commit()


def buscar_por_nome(conn, termo, ordenar="nome"):
    """Tela de busca. 'termo' e 'ordenar' vem da URL: /clientes?q=...&ordenar=nome|cidade"""
    coluna = COLUNAS_ORDENAVEIS.get(ordenar)
    if coluna is None:
        raise ValueError(f"ordenacao invalida: {ordenar!r}")
    sql = f"SELECT id, nome, cidade FROM clientes WHERE nome LIKE ? ORDER BY {coluna}"
    return conn.execute(sql, (f"%{termo}%",)).fetchall()


def buscar_por_cidade(conn, cidade):
    """Filtro por cidade do relatorio regional (vem do campo de texto do relatorio)."""
    sql = "SELECT id, nome, cidade FROM clientes WHERE cidade = ? ORDER BY nome"
    return conn.execute(sql, (cidade,)).fetchall()
