from machine import Pin, SoftSPI  # Alterado para SoftSPI para permitir a mistura de pinos
import os
import time
import sdcard

# =========================
# SPI (Emulação por Software)
# =========================
spi = SoftSPI(                # Removido o número do barramento (0)
    baudrate=1_000_000,
    polarity=0,
    phase=0,
    sck=Pin(2),
    mosi=Pin(3),
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