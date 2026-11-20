from datetime import timedelta

from fusos import para_local, para_utc


def agendar_diario(primeiro_local, fuso, quantidade):
    """Lembrete diario no mesmo horario local do cliente.

    Devolve os instantes em UTC que vao para a fila de envio. A soma dos dias
    e feita no horario local, para atravessar a mudanca de horario de verao.
    """
    return [para_utc(primeiro_local + timedelta(days=i), fuso) for i in range(quantidade)]


def texto_lembrete(momento_utc, fuso, titulo):
    local = para_local(momento_utc, fuso)
    return f"{titulo} - {local:%d/%m/%Y %H:%M}"


def eventos_do_dia(eventos, dia_local, fuso):
    """eventos: lista de (momento_utc, titulo); dia_local: date no fuso do cliente."""
    return [titulo for momento, titulo in eventos if para_local(momento, fuso).date() == dia_local]
