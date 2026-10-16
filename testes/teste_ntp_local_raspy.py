
import network
import ntptime
import time

# Configuração do hotspot da Raspberry Pi
SSID = "Wifi-BMS"
PASSWORD = "testebms2026"

WIFI_SSID = "Wifi-BMS"
WIFI_PASSWORD = "testebms2026"

# Servidor NTP da raspy
ntptime.host = "10.42.0.1"

def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Conectando ao hotspot...")
        wlan.connect(SSID, PASSWORD)

        timeout = 20
        inicio = time.time()

        while not wlan.isconnected():
            if time.time() - inicio >= timeout:
                raise RuntimeError("Falha ao conectar ao Wi-Fi")
            time.sleep(1)

    print("Wi-Fi conectado!")
    print("IP da Pico W:", wlan.ifconfig()[0])
    return wlan


def sincronizar_horario(tentativas=5):
    for tentativa in range(tentativas):
        try:
            print("Sincronizando com ntp.unicamp.br...")
            ntptime.settime()

            # O ntptime normalmente ajusta o relógio para UTC
            print("Relógio sincronizado!")
            print("UTC:", time.localtime())
            return True

        except Exception as erro:
            print("Falha NTP:", erro)
            time.sleep(2)

    return False


conectar_wifi()

if not sincronizar_horario():
    print("AVISO: não foi possível sincronizar o horário.")
