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

def enviar_dados(dados, GOOGLE_SCRIPT_URL):

    resposta = None

    try:

        print()
        print("Enviando dados...")

        resposta = requests.post(
            GOOGLE_SCRIPT_URL,
            json=dados
        )

        print("Status:", resposta.status_code)

        print("Resposta:")
        print(resposta.text)

        if resposta.status_code == 200:
            print("ENVIO OK")
            return True

        elif resposta.status_code in (301, 302, 303, 307, 308):

            print("Google retornou redirecionamento")

            location = resposta.headers.get("Location")

            print("Location:")
            print(location)

            resposta.close()
            resposta = None

            if location is None:
                print("ERRO: Location não encontrado")
                return False

            print("Enviando novamente para o endereço redirecionado...")

            resposta = requests.post(
                location,
                json=dados
            )

            print("Status final:", resposta.status_code)
            print("Resposta final:")
            print(resposta.text)

            if resposta.status_code == 200:
                print("ENVIO OK")
                return True

            return False

        else:
            print("ERRO HTTP")
            return False

    except Exception as e:

        print()
        print("ERRO AO ENVIAR:")
        print(e)

        return False

    finally:

        if resposta is not None:
            resposta.close()
