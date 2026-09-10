from machine import Pin, I2C
import time


# ============================================================
# ADS1115
# ============================================================

class ADS1115:

    def __init__(self, i2c, address=0x48):
        self.i2c = i2c
        self.address = address

        self.REG_CONVERSION = 0x00
        self.REG_CONFIG = 0x01

    def read(self, channel):

        if channel < 0 or channel > 3:
            raise ValueError("Canal deve ser 0, 1, 2 ou 3")

        # ----------------------------------------------------
        # MUX - Single Ended
        #
        # A0 = 100
        # A1 = 101
        # A2 = 110
        # A3 = 111
        # ----------------------------------------------------

        mux = 0x4000 + (channel << 12)

        # ----------------------------------------------------
        # Configuração
        #
        # Bit 15 = 1 -> inicia conversão
        #
        # PGA = ±4.096 V
        # MODE = single-shot
        # DR = 128 SPS
        # Comparator desabilitado
        # ----------------------------------------------------

        config = (
            0x8000 |      # OS
            mux |         # MUX
            0x0200 |      # PGA ±4.096 V
            0x0100 |      # MODE single-shot
            0x0080 |      # 128 SPS
            0x0003        # comparator disabled
        )

        # ----------------------------------------------------
        # Escreve no registrador CONFIG
        # ----------------------------------------------------

        self.i2c.writeto_mem(
            self.address,
            self.REG_CONFIG,
            bytes([
                (config >> 8) & 0xFF,
                config & 0xFF
            ])
        )

        # ----------------------------------------------------
        # Aguarda conversão
        # ----------------------------------------------------

        time.sleep_ms(10)

        # ----------------------------------------------------
        # Lê registrador de conversão
        # ----------------------------------------------------

        data = self.i2c.readfrom_mem(
            self.address,
            self.REG_CONVERSION,
            2
        )

        value = (data[0] << 8) | data[1]

        # Signed 16 bits
        if value & 0x8000:
            value -= 65536

        return value


# ============================================================
# I2C
# ============================================================

i2c = I2C(
    0,
    scl=Pin(9),
    sda=Pin(8),
    freq=100000
)


# ============================================================
# Scanner I2C
# ============================================================

print()
print("Dispositivos I2C encontrados:")

devices = i2c.scan()

for device in devices:
    print("  Endereço:", hex(device))

print()


# ============================================================
# ADS1115
# ============================================================

ads = ADS1115(
    i2c,
    address=0x48
)


# ============================================================
# TESTE
# ============================================================

while True:

    print("----- ADS1115 -----")

    for canal in range(4):

        try:

            raw = ads.read(canal)

            voltage = raw * 4.096 / 32768
            
            temp = 0.0030908 * raw - 25.04

            print(
                "A{}: {:6d}  {:.4f} V  {:.2f}".format(
                    canal,
                    raw,
                    voltage,
                    temp
                )
            )

        except OSError as e:

            print(
                "A{}: ERRO I2C -> {}".format(
                    canal,
                    e
                )
            )

    print("-------------------")
    print()

    time.sleep(1)