import network
import time
import requests

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




# ============================================================
# ENVIAR DADOS
# ============================================================

def enviar_dados(dados, URL_DADOS):
    try:

        resposta = requests.post(
            URL_DADOS,
            json=dados
        )

        print("Status:", resposta.status_code)
        print("Resposta:", resposta.text)

        resposta.close()

    except Exception as e:

        print("Erro:")
        print(e)