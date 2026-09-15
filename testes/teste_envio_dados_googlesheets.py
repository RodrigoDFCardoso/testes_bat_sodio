import network
import time
import requests

# ============================================================
# CONFIGURAÇÕES
# ============================================================

WIFI_SSID = "Ap1208_2G"
WIFI_PASSWORD = "20081995"

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbw1nrq_VxDu4h3HfKFV7st50TZeyFlTf_Q5lS56WCayw0TNry8xzH7mTLwLyH6m6QJAtg/exec"

# ============================================================
# CONECTAR AO WI-FI
# ============================================================

def conectar_wifi():

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

def enviar_dados(dados):

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


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

print()
print("==============================")
print(" TESTE PICO W + GOOGLE SHEETS")
print("==============================")

# Conecta ao Wi-Fi
wifi = conectar_wifi()

if wifi is None:
    print("Não foi possível conectar ao Wi-Fi")
else:

    # Dados de teste
    dados = {
        "timestamp": time.time() + 3* 3600,

        "cell_A": 3.214,
        "cell_B": 3.194,
        "cell_C": 3.224,
        "cell_D": 3.204,

        "current": 0.1984,
        "power": 2.574,

        "temp_A": 25.44,
        "temp_B": 25.74,
        "temp_C": 25.54,
        "temp_D": 25.84
    }

    # Envia
    sucesso = enviar_dados(dados)

    print()

    if sucesso:
        print("==============================")
        print(" TESTE CONCLUIDO COM SUCESSO")
        print("==============================")
    else:
        print("==============================")
        print(" FALHA NO ENVIO")
        print("==============================")