# ================================================================
#  Funções para o INA226
#  Observação:
#   - Este exemplo não usa o registrador de CALIBRAÇÃO do INA226.
#     Em vez disso, calcula a corrente como Vshunt/Rshunt manualmente.
#     Isso é válido, mas perde a leitura direta do registrador CURRENT/POWER
#     já calibrados pelo INA. Se quiser usar CURRENT/POWER, programe CALIBRATION_REG.
# ================================================================

# ================================================================
#  INA226 (medidor de tensão de barramento e queda no shunt)
# ================================================================

from machine import PWM, Pin  # PWM, GPIO
from machine import SoftI2C, ADC
import time

shunt_resistor = 0.1

i2c = SoftI2C(scl=Pin(19), sda=Pin(18))

INA226_ADDR = 68            # Endereço padrão
# Registradores do INA226
CONFIG_REG         = 0x00
SHUNT_VOLTAGE_REG  = 0x01
BUS_VOLTAGE_REG    = 0x02
POWER_REG          = 0x03
CURRENT_REG        = 0x04
CALIBRATION_REG    = 0x05


def configurar_ina226(INA226_ADDR):
    """
    Configura o INA226 para modo contínuo de medição, com média/prazos default.
    0x4127 é um exemplo comum: shunt/bus ADC = 1.1ms, média=1, continuous.
    Ajuste se precisar de mais filtragem (média) ou rapidez.
    """
    config = 0x4127
    i2c.writeto_mem(INA226_ADDR, CONFIG_REG, bytearray([config >> 8, config & 0xFF]))

def ler_tensao_bus(INA226_ADDR):
    """
    Lê a tensão do barramento (VBUS).
    Conversão do INA226: 1.25 mV/bit → multiplicador 1.25/1000 para Volts.
    """
    data = i2c.readfrom_mem(INA226_ADDR, BUS_VOLTAGE_REG, 2)
    raw = (data[0] << 8) | data[1]
    bus_voltage = raw * 1.25 / 1000.0  # V
    return bus_voltage

def ler_tensao_shunt(INA226_ADDR):
    """
    Lê a tensão no resistor shunt.
    Conversão do INA226: 2.5 µV/bit e valor é assinado (2’s complement em 16 bits).
    """
    data = i2c.readfrom_mem(INA226_ADDR, SHUNT_VOLTAGE_REG, 2)
    raw = (data[0] << 8) | data[1]
    if raw > 32767:
        raw -= 65536  # converte para valor assinado
    shunt_voltage = raw * 2.5 / 1_000_000.0  # V
    return shunt_voltage

def ler_corrente(INA226_ADDR):
    """
    Calcula corrente a partir de Vshunt/Rshunt.
    Sinal:
      - Dependendo da orientação do shunt, a leitura pode sair negativa.
      - Aqui invertemos o sinal para mostrar positivo ao consumo "convencional".
    Retorna em mA.
    """
    vsh = ler_tensao_shunt(INA226_ADDR)
    i = vsh / shunt_resistor          # A (com sinal)
    i_mA = -i * 1000.0                # inverte o sinal
    return i_mA

def calcular_potencia(v_bus, corrente_mA):
    """
    Potência aproximada: P = V * I.
    A corrente está em mA ⇒ convertemos para A.
    Retorno em mW (mais prático para painéis pequenos).
    """
    p_w = v_bus * (corrente_mA / 1000.0)  # W
    return p_w * 1000.0                    # mW

# Função utilitária: mapeamento linear de faixa
def map_value(value, in_min, in_max, out_min, out_max):
    """
    Mapeia 'value' da faixa [in_min, in_max] para [out_min, out_max].
    Usamos // (inteiro) pois os índices de LEDs devem ser inteiros.
    """
    return (value - in_min) * (out_max - out_min) // (in_max - in_min) + out_min


'''
#testar e depois excluir este while

 # ----------------------------------------
# 6) Teste do INA226 (somente V7 com INA226 populado)
# ----------------------------------------
configurar_ina226(INA226_ADDR)

# Valor do shunt (Ohms). Ajuste para o valor real do hardware!

# Loop de medição contínua (1/s)
while True:
    v_bus     = ler_tensao_bus(INA226_ADDR)
    corrente  = ler_corrente(INA226_ADDR)      # mA
    potencia  = calcular_potencia(v_bus, corrente) # mW
    #exibir_no_oled(v_bus, corrente, potencia)
    print("V: {:.2f}V".format(v_bus))
    print("I: {:+.2f}mA".format(corrente))
    print("P: {:+.2f}mW".format(potencia))
    print("Shunt:{:+.3f}mV".format(ler_tensao_shunt(INA226_ADDR) * -1000.0))

    time.sleep(1)

'''