class Pedido:
    def __init__(self, cliente, itens=[], cupons=set()):
        self.cliente = cliente  # e-mail do cliente
        self.itens = itens
        self.cupons = cupons

    def adicionar(self, produto, quantidade, preco_centavos):
        self.itens.append((produto, quantidade, preco_centavos))

    def aplicar_cupom(self, codigo):
        self.cupons.add(codigo)

    def total_centavos(self):
        return sum(q * p for _, q, p in self.itens)
