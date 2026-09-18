from machine import Pin, I2C
import time


# ============================================================
# I2C
# ============================================================

dev = I2C(
    0,
    scl=Pin(9),
    sda=Pin(8)
)


# ============================================================
# Endereço ADS1115
# 72 decimal = 0x48
# ============================================================

address = 72


# ============================================================
# Leitura do registrador CONFIG
# ============================================================

def readConfig():

    dev.writeto(
        address,
        bytearray([1])
    )

    result = dev.readfrom(
        address,
        2
    )

    return (result[0] << 8) | result[1]


# ============================================================
# Leitura de um canal do ADS1115
# Resistor de ganho INA122 = 33k 1% 1/10 W - ganho aproximado de 11
# channel:
# 0 -> A0 -> Sensor 4 (D)
# 1 -> A1 -> Sensor 2 (B)
# 2 -> A2 -> Sensor 3 (C)
# 3 -> A3 -> Sensor 1 (A)
# ============================================================

def readValueFrom(channel):

    # Lê configuração atual
    config = readConfig()

    # --------------------------------------------------------
    # Limpa MUX
    # Bits 14:12
    # --------------------------------------------------------

    config &= ~(7 << 12)

    # --------------------------------------------------------
    # Limpa PGA
    # Bits 11:9
    # --------------------------------------------------------

    config &= ~(7 << 9)

    # --------------------------------------------------------
    # Configura canal single-ended
    #
    # A0 -> 100
    # A1 -> 101
    # A2 -> 110
    # A3 -> 111
    # --------------------------------------------------------

    config |= (4 + channel) << 12

    # --------------------------------------------------------
    # Inicia nova conversão
    # --------------------------------------------------------

    config |= (1 << 15)

    # --------------------------------------------------------
    # PGA = ±4.096 V
    # --------------------------------------------------------

    config |= (1 << 9)

    # --------------------------------------------------------
    # Divide configuração em dois bytes
    # --------------------------------------------------------

    config_bytes = [
        (config >> 8) & 0xFF,
        config & 0xFF
    ]

    # --------------------------------------------------------
    # Escreve no registrador CONFIG
    # --------------------------------------------------------

    dev.writeto(
        address,
        bytearray([1] + config_bytes)
    )

    # --------------------------------------------------------
    # Aguarda conversão
    # --------------------------------------------------------

    config = readConfig()

    while (config & 0x8000) == 0:
        config = readConfig()

    # --------------------------------------------------------
    # Lê registrador de conversão
    # --------------------------------------------------------

    dev.writeto(
        address,
        bytearray([0])
    )

    result = dev.readfrom(
        address,
        2
    )

    # Converte os dois bytes para inteiro
    value = (result[0] << 8) | result[1]

    # --------------------------------------------------------
    # Converte para signed 16 bits
    # --------------------------------------------------------

    if value & 0x8000:
        value -= 65536

    return value


# ============================================================
# Conversão RAW -> tensão
#
# PGA = ±4.096 V
# ============================================================

def voltage(val):

    return val * 4.096 / 32768


def get_value(channel):
    try:

        value = readValueFrom(channel)

        value_voltage = voltage(value)
        
        # temp = 0.00309077 * value
        temp = 0.004103 * value - 2.394287

        return value, value_voltage, temp

    except Exception as e:

        print(
            "A{}: ERRO -> {}".format(
                channel,
                e
            )
        )