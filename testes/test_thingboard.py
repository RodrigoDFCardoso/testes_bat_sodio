import network
import time
import requests
import random
import ntptime

import lib_save_sdcard as save_local

# curl -v -X POST http://thingsboard.cloud/api/v1/TPoUBv8x6rCMwLUqLBr5/telemetry --header Content-Type:application/json --data "{temperature:25}"

# ============================================================
# CONFIGURAÇÕES
# ============================================================

WIFI_SSID = "Ap1208_2G"
WIFI_PASSWORD = "20081995"

THINGSBOARD_HOST = "https://thingsboard.cloud"

ACCESS_TOKEN = "TPoUBv8x6rCMwLUqLBr5"

URL = THINGSBOARD_HOST + "/api/v1/" + ACCESS_TOKEN + "/telemetry"

#curl -v -X POST http://192.168.18.34:8080/api/v1/QmCB4MQiSFWugvtePeaN/telemetry --header Content-Type:application/json --data "{temperature:25}"

# https://thingsboard.io/docs/installation/docker/

# teste thingsboard local
URL = "http://192.168.18.34:8080/api/v1/QmCB4MQiSFWugvtePeaN/telemetry"

# ============================================================
# CONECTAR AO WI-FI
# ============================================================

def conectar_wifi(WIFI_SSID, WIFI_PASSWORD):

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if wlan.isconnected():
        print("Wi-Fi já conectado")
        print("IP:", wlan.ifconfig()[0])
        return wlan

    print("Conectando ao Wi-Fi...")

    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    timeout = 20
    inicio = time.time()

    while not wlan.isconnected():

        if time.time() - inicio > timeout:
            print("ERRO: timeout ao conectar no Wi-Fi")
            return None

        print(".", end="")
        time.sleep(1)

    print()
    print("Wi-Fi conectado!")
    print("IP:", wlan.ifconfig()[0])
    print("Mascara:", wlan.ifconfig()[1])
    print("Gateway:", wlan.ifconfig()[2])
    print("DNS:", wlan.ifconfig()[3])

    return wlan

conectar_wifi(WIFI_SSID, WIFI_PASSWORD)

# dados = {
#     "timestamp": time.time() + 3* 3600,
#     "channel": "A",
#     "temp": 25.4,
#     "voltage": 3.21,
#     "current": 198.0,
#     "power": 635.0
# }
ntptime.settime()
while True:
    
    for dado in ["A", "B", "C", "D"]:
        voltage = random.uniform(1.2, 4.2)
        current = random.uniform(-900.0, 900.0)
        temp = random.uniform(-10, 100)
        dado_envio = {
            "timestamp": time.time(),

            "channel": dado,
            "temp": temp,
            "voltage": voltage,
            "current": current,

            "power": voltage * current
        }
        
        dados_local = [time.time(), dado, temp, voltage, current, voltage * current]
        save_local.salvar_dados(dados_local)
        try:

            resposta = requests.post(
                URL,
                json=dado_envio
            )

            print("Status:", resposta.status_code)
            print("Resposta:", resposta.text)

            resposta.close()

        except Exception as e:

            print("Erro:")
            print(e)

    time.sleep(1)
