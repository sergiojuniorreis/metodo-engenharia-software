class TimeoutGateway(Exception):
    """O gateway nao respondeu a tempo. A cobranca pode ou nao ter sido efetivada."""


class GatewaySimulado:
    """Gateway de pagamento de homologacao; segue o contrato do gateway real.

    cobrar(valor_centavos, chave_idempotencia=None) -> id da transacao.
    Se uma chave_idempotencia ja usada for enviada de novo, o gateway devolve a
    transacao original em vez de cobrar outra vez.

    timeouts_antes: quantas chamadas falham antes de chegar ao banco emissor.
    timeouts_depois: quantas chamadas cobram, mas a resposta se perde (timeout).
    """

    def __init__(self, timeouts_antes=0, timeouts_depois=0):
        self.timeouts_antes = timeouts_antes
        self.timeouts_depois = timeouts_depois
        self.chamadas = 0
        self.cobrancas = []  # (transacao, valor_centavos) efetivamente cobradas
        self._por_chave = {}

    def cobrar(self, valor_centavos, chave_idempotencia=None):
        self.chamadas += 1
        if self.timeouts_antes > 0:
            self.timeouts_antes -= 1
            raise TimeoutGateway()
        if chave_idempotencia is not None and chave_idempotencia in self._por_chave:
            transacao = self._por_chave[chave_idempotencia]
        else:
            transacao = f"tx{len(self.cobrancas) + 1}"
            self.cobrancas.append((transacao, valor_centavos))
            if chave_idempotencia is not None:
                self._por_chave[chave_idempotencia] = transacao
        if self.timeouts_depois > 0:
            self.timeouts_depois -= 1
            raise TimeoutGateway()
        return transacao
