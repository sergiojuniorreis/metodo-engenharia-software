from datetime import timedelta, timezone

# Deslocamento de cada fuso atendido, em horas, em relacao ao UTC.
DESLOCAMENTOS = {
    "America/Sao_Paulo": -3,
    "America/Manaus": -4,
    "Europe/Lisbon": 0,
    "America/New_York": -5,
}


def para_local(momento_utc, fuso):
    """Converte um datetime UTC (com tzinfo) para o horario local do fuso (sem tzinfo)."""
    return (momento_utc + timedelta(hours=DESLOCAMENTOS[fuso])).replace(tzinfo=None)


def para_utc(momento_local, fuso):
    """Converte um horario local do fuso (sem tzinfo) para datetime UTC (com tzinfo)."""
    return (momento_local - timedelta(hours=DESLOCAMENTOS[fuso])).replace(tzinfo=timezone.utc)
