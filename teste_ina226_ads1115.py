from machine import Pin, I2C, SoftI2C
import time

# =========================================================
# I2C - ADS1115
# =========================================================

i2c_ads = I2C(
    0,
    scl=Pin(9),
    sda=Pin(8),
    freq=400000
)

ADS_ADDRESS = 72


# =========================================================
# I2C - INA226
# =========================================================

i2c_ina226 = SoftI2C(
    scl=Pin(19),
    sda=Pin(18)
)

# INA226
options = {
    0: ['D', 76],
    1: ['C', 72],
    2: ['B', 68],
    3: ['A', 64]
}


# =========================================================
# FUNÇÕES ADS1115
# =========================================================

def inicializar_ads1115():
    """
    Inicializa o ADS1115.
    """

    dev = I2C(
        0,
        scl=Pin(9),
        sda=Pin(8),
        freq=400000
    )

    return dev


def ler_ads1115(dev, canal):
    """
    Realiza a leitura de um canal do ADS1115.

    canal:
        0 -> A0
        1 -> A1
        2 -> A2
        3 -> A3
    """

    # Aqui entra a leitura conforme
    # a biblioteca do ADS1115 utilizada.

    valor = dev.readfrom_mem(
        ADS_ADDRESS,
        0x00,
        2
    )

    return valor


# =========================================================
# FUNÇÕES INA226
# =========================================================

def inicializar_ina226():
    """
    Inicializa o barramento dos INA226.
    """

    i2c = SoftI2C(
        scl=Pin(19),
        sda=Pin(18)
    )

    return i2c


def listar_ina226(i2c):
    """
    Verifica quais INA226 estão presentes no barramento.
    """

    print("INA226 encontrados:")

    for numero, dados in options.items():

        nome = dados[0]
        endereco = dados[1]

        dispositivos = i2c.scan()

        if endereco in dispositivos:
            print(
                "INA226 {} - endereco {} (0x{:02X})".format(
                    nome,
                    endereco,
                    endereco
                )
            )


def ler_ina226(i2c, endereco):
    """
    Realiza leitura do INA226.

    endereco:
        64, 68, 72 ou 76

    Retorna:
        tensao
        corrente
    """

    # Aqui entra a leitura conforme
    # a biblioteca do INA226 utilizada.

    return 0, 0