import network
import time
import requests
import ntptime
from machine import Pin, I2C, SoftI2C, PWM, ADC # confirmar uso de PWM e ADC
from machine import RTC

# Fuso horário de Brasília
UTC_OFFSET = -3 * 60 * 60

# libs minha
import lib_send_data as send
import lib_ads1115_get_data as ads1115
import lib_ina226_get_data as ina226
import lib_oled as oled


## enderecos ina's e posicao adc
#options = {0 : ['D', 76, 0], 1 : ['C', 72, 2], 2 : ['B', 68, 1], 3 : ['A', 64, 3]}

#options = {2 : ['B', 68, 1], 3 : ['A', 64, 3]}

options = {3 : ['A', 64, 3]}
# ============================================================
# Leitura de um canal do ADS1115
# Resistor de ganho INA122 = 33k 1% 1/10 W - ganho aproximado de 11
# channel:
# 0 -> A0 -> Sensor 4 (D)
# 1 -> A1 -> Sensor 2 (B)
# 2 -> A2 -> Sensor 3 (C)
# 3 -> A3 -> Sensor 1 (A)
# ============================================================

# ============================================================
# CONFIGURAÇÕES
# ============================================================

#WIFI_SSID = "Ap1208_2G"
#WIFI_PASSWORD = "20081995"

WIFI_SSID = "Wifi BMS"
WIFI_PASSWORD = "testebms2024"

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxpPVJgj-tuBg3B9PkMabwlyUM02s5aTYDSF29srKwAfO5FiZ5_H7hCgy6WplV_nc1__A/exec"

THINGSBOARD_HOST = "https://thingsboard.cloud"

ACCESS_TOKEN = "TPoUBv8x6rCMwLUqLBr5"

THINGSBOARD_URL = THINGSBOARD_HOST + "/api/v1/" + ACCESS_TOKEN + "/telemetry"

URL = GOOGLE_SCRIPT_URL

# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

print()
print("==============================")
print(" TESTE PICO W + BMS")
print("==============================")

# Conecta ao Wi-Fi
wifi = send.conectar_wifi(WIFI_SSID, WIFI_PASSWORD)


oled.scroll_text("Conectando WIFI")


# wifi = True

if wifi is None:
    # print("Não foi possível conectar ao Wi-Fi")
    status_wifi = "OFF"
else:
    status_wifi = "ON"
    ntptime.settime()
    while True:
        # corrigir ina e sensor de temperatura correspondente
        # filtrar erros para eventuais problemas (faltando)
        status_dados = "NO"
        sucesso = "---"
        oled.update_massages(status_wifi, status_dados, sucesso)
        for i in options:
            sucesso = "_-_"
            ina226.configurar_ina226(options[i][1]) # para cada endereco do ina226 uma config é feita
            #i = 3
            temp = ads1115.get_value(i)
            v_bus = ina226.ler_tensao_bus(options[i][1])
            corrente_mA = ina226.ler_corrente(options[i][1])

            dado_envio = {
                "timestamp": time.time(),
                "channel": options[i][0],
                "temp": round(temp[2], 2),
                "voltage": round(v_bus, 3),
                "current": round(corrente_mA, 3),

                "power": round(ina226.calcular_potencia(v_bus, corrente_mA), 3)
            }

            if all(value is not None and value != "" for value in dado_envio.values()):
                status_dados = 'OK'

            # print(dado_envio) # testar como o print vai ficar antes de preencher a planilha

            # Envia
            #sucesso = send.enviar_dados(dado_envio, THINGSBOARD_URL)
            sucesso = send.enviar_dados(dado_envio, URL)
            # sucesso = send.enviar_dados(dado_envio, URL)
            oled.update_massages(status_wifi, status_dados, sucesso)
            # print()

        time.sleep(5) #define a frequencia com que será enviado os dados
