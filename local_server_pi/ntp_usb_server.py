import serial
import time
from datetime import datetime

PORT = "COM7"  #/dev/ttyACM0
BAUDRATE = 115200

print("BMS-SODIO - USB NTP Server")
print("Porta:", PORT)
print("Aguardando requisicoes do Pico W...")

while True:
    ser = None

    try:
        ser = serial.Serial(
            port=PORT,
            baudrate=BAUDRATE,
            timeout=1,
            write_timeout=2
        )

        print("Pico W conectado!")

        while True:
            linha = ser.readline()

            if not linha:
                continue

            print("RECEBIDO:", repr(linha))

            request = linha.decode(
                "ascii", errors="ignore"
            ).strip()

            if request == "NTP?":
                now = datetime.now().astimezone()

                response = (
                    f"TIME,{now.year},{now.month},"
                    f"{now.day},{now.hour},"
                    f"{now.minute},{now.second}\n"
                )

                ser.write(response.encode("ascii"))
                ser.flush()

                print("ENVIADO:", response.strip())

    except serial.SerialException as erro:
        print("Erro na comunicacao:", erro)
        time.sleep(3)

    except KeyboardInterrupt:
        print("Servidor encerrado.")
        break

    finally:
        if ser is not None and ser.is_open:
            ser.close()
