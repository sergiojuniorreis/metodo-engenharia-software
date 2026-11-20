class Pedido:
    def __init__(self, cliente, itens=None, cupons=None):
        self.cliente = cliente  # e-mail do cliente
        self.itens = list(itens) if itens is not None else []
        self.cupons = set(cupons) if cupons is not None else set()

    def adicionar(self, produto, quantidade, preco_centavos):
        self.itens.append((produto, quantidade, preco_centavos))

    def aplicar_cupom(self, codigo):
        self.cupons.add(codigo)

    def total_centavos(self):
        return sum(q * p for _, q, p in self.itens)
