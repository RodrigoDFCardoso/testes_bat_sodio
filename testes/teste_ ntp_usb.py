import sys
import time
import machine
import select
import lib_oled as oled

rtc = machine.RTC()
d = 0

def sincronizar_horario(timeout=5):
    print("Solicitando horario ao servidor USB...")
    oled.update_massages("tes", "sol", "nada", "ainda")

    poll = select.poll()
    poll.register(sys.stdin, select.POLLIN)

    inicio = time.ticks_ms()
    x = 0

    sys.stdout.write("NTP?\n")
    

    while time.ticks_diff(time.ticks_ms(), inicio) < timeout * 1000:

        eventos = poll.poll(100)

        if eventos:
            resposta = sys.stdin.readline().strip()

            if not resposta:
                continue

            if resposta.startswith("TIME,"):
                try:
                    dados = resposta.split(",")

                    if len(dados) != 7:
                        raise ValueError("Quantidade de campos invalida")

                    ano, mes, dia = map(int, dados[1:4])
                    hora, minuto, segundo = map(int, dados[4:7])

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

                    weekday = time.localtime(
                        time.mktime(
                            (ano, mes, dia, 0, 0, 0, 0, 0)
                        )
                    )[6]

                    rtc.datetime((
                        ano, mes, dia, weekday,
                        hora, minuto, segundo, 0
                    ))

                    timestamp = time.time()

                    print("RTC atualizado com sucesso!")
                    print("Data/hora:", rtc.datetime())
                    print("Unix Timestamp:", timestamp)

                    oled.update_massages(
                        "Unix",
                        timestamp,
                        hora,
                        minuto
                    )

                    return (
                        True, ano, mes, dia,
                        hora, minuto, segundo, timestamp
                    )

                except Exception as erro:
                    print("Erro ao interpretar horario:", erro)
                    oled.update_massages("erro", "resp", erro, x)

                    return (False, None, None, None,
                            None, None, None, None)

        x += 1

    print("Servidor USB nao respondeu.")
    oled.update_massages("serev", "erro", d, x)

    return (False, None, None, None,
            None, None, None, None)


print("BMS-SODIO - Cliente USB NTP")

while True:

    resultado = sincronizar_horario()

    if resultado[0]:

        _, ano, mes, dia, hora, minuto, segundo, timestamp = resultado

        print("Sincronizacao concluida.")
        print("Data:", dia, mes, ano)
        print("Hora:", hora, minuto, segundo)
        print("Unix Timestamp:", timestamp)

        break

    d += 1
    time.sleep(5)

