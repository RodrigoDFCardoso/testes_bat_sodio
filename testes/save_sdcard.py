from machine import Pin, SPI
import os
import time

# =========================
# SPI
# =========================
spi = SPI(
    0,
    baudrate=1_000_000,
    polarity=0,
    phase=0,
    sck=Pin(18),
    mosi=Pin(19),
    miso=Pin(16)
)

# Chip Select
cs = Pin(17, Pin.OUT)

# =========================
# Inicializa cartão SD
# =========================
import sdcard

sd = sdcard.SDCard(spi, cs)

# Monta o sistema de arquivos
os.mount(sd, "/sd")

print("Cartão SD montado!")
print("Arquivos:", os.listdir("/sd"))

# =========================
# Teste de gravação
# =========================

arquivo = "/sd/teste.txt"

contador = 0

while contador <= 5:

    contador += 1

    texto = "Teste SD - registro {}\n".format(contador)

    with open(arquivo, "a") as f:
        f.write(texto)

    print("Gravado:", texto.strip())

    time.sleep(2)