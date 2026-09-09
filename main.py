import network
import time
import requests
from machine import Pin, I2C, SoftI2C, PWM, ADC # confirmar uso de PWM e ADC

# libs minha
import lib_send_data as send
import lib_ads1115_get_data as ads1115
import lib_ina226_get_data as ina226


## enderecos ina's
options = {0 : ['D', 76], 1 : ['C', 72], 2 : ['B', 68], 3 : ['A', 64]}

# ============================================================
# Leitura de um canal do ADS1115
#
# channel:
# 0 -> A0
# 1 -> A1
# 2 -> A2
# 3 -> A3
# ============================================================

# ============================================================
# CONFIGURAÇÕES
# ============================================================

# WIFI_SSID = "Ap1208_2G"
# WIFI_PASSWORD = "20081995"

WIFI_SSID = "Wifi BMS"
WIFI_PASSWORD = "testebms2024"

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxpPVJgj-tuBg3B9PkMabwlyUM02s5aTYDSF29srKwAfO5FiZ5_H7hCgy6WplV_nc1__A/exec"


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

print()
print("==============================")
print(" TESTE PICO W + GOOGLE SHEETS")
print("==============================")

# Conecta ao Wi-Fi
wifi = send.conectar_wifi(WIFI_SSID, WIFI_PASSWORD)

# wifi = True

if wifi is None:
    print("Não foi possível conectar ao Wi-Fi")
else:

    while True:
        # corrigir ina e sensor de temperatura correspondente
        # filtrar erros para eventuais problemas (faltando)
        for i in range(4):
            ina226.configurar_ina226(options[i][1]) # para cada endereco do ina226 uma config é feita

            temp = ads1115.get_value(i)
            v_bus = ina226.ler_tensao_bus(options[i][1])
            corrente_mA = ina226.ler_corrente(options[i][1])

            dado_envio = {
                "timestamp": time.time() + 3* 3600,
                "channel": options[i][0],
                "temp": temp[1], # falta converter tensao para temperatura
                "voltage": v_bus,
                "current": corrente_mA,

                "power": ina226.calcular_potencia(v_bus, corrente_mA)
            }

            print(dado_envio) # testar como o print vai ficar antes de preencher a planilha

            # Envia
            sucesso = send.enviar_dados(dado_envio, GOOGLE_SCRIPT_URL)
            # sucesso = True

            print()

            if sucesso:
                print("==============================")
                print(" TESTE CONCLUIDO COM SUCESSO")
                print("==============================")
            else:
                print("==============================")
                print(" FALHA NO ENVIO")
                print("==============================")
                
                
        print("fim dos dados for")

        time.sleep(10) #define a frequencia com que será enviado os dados
