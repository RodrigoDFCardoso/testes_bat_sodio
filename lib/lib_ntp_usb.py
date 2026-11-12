
import sys
import time
import machine
import select


rtc = machine.RTC()


def sincronizar_horario(timeout=5):
    """
    Solicita data/hora ao servidor USB.
    Atualiza o RTC interno do Pico W.
    Retorna True se a sincronização for concluída.
    """

    print("Solicitando horario ao servidor USB...")

    poll = select.poll()
    poll.register(sys.stdin, select.POLLIN)

    inicio = time.ticks_ms()

    # Solicita horario ao servidor
    sys.stdout.write("NTP?\n")

    while time.ticks_diff(time.ticks_ms(), inicio) < timeout * 1000:

        eventos = poll.poll(100)

        if not eventos:
            continue

        resposta = sys.stdin.readline().strip()

        if not resposta.startswith("TIME,"):
            continue

        try:
            dados = resposta.split(",")

            if len(dados) != 7:
                raise ValueError("Quantidade de campos invalida")

            ano, mes, dia = map(int, dados[1:4])
            hora, minuto, segundo = map(int, dados[4:7])

            # Validacao dos campos
            if not (2025 <= ano <= 2100):
                raise ValueError("Ano invalido")

            if not (1 <= mes <= 12):
                raise ValueError("Mes invalido")

            if not (1 <= dia <= 31):
                raise ValueError("Dia invalido")

            if not (0 <= hora <= 23):
                raise ValueError("Hora invalida")

            if not (0 <= minuto <= 59):
                raise ValueError("Minuto invalido")

            if not (0 <= segundo <= 59):
                raise ValueError("Segundo invalido")

            # Calcula dia da semana
            weekday = time.localtime(
                time.mktime(
                    (ano, mes, dia, 0, 0, 0, 0, 0)
                )
            )[6]

            # Atualiza RTC interno
            rtc.datetime((
                ano, mes, dia, weekday,
                hora, minuto, segundo, 0
            ))

            print("RTC atualizado com sucesso!")
            print("Data/hora:", rtc.datetime())

            return True

        except Exception as erro:
            print("Erro ao interpretar horario:", erro)
            return False

    print("Servidor USB nao respondeu.")
    return False


def obter_timestamp():
    """Retorna timestamp Unix em segundos."""
    return time.time()


def obter_data_hora():
    """Retorna data e hora do RTC."""
    return rtc.datetime()

