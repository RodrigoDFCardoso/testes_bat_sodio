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
    sck=Pin(28),
    mosi=Pin(17),
    miso=Pin(16)
)

# Chip Select
cs = Pin(1, Pin.OUT)

# =========================
# Inicializa cartão SD
# =========================
try:
    sd = sdcard.SDCard(spi, cs)

    # Monta o sistema de arquivos (Usa VfsFat para garantir compatibilidade)
    vfs = os.VfsFat(sd)
    os.mount(vfs, "/sd")

    print("Cartão SD montado!")
    print("Arquivos:", os.listdir("/sd"))

    # =========================
    # Teste de gravação
    # =========================
    arquivo = "/sd/teste.txt"
    contador = 0

    while contador < 5:  # Ajustado para parar exatamente após 5 registros

        contador += 1
        texto = "Teste SD - registro {}\n".format(contador)

        with open(arquivo, "a") as f:
            f.write(texto)

        print("Gravado:", texto.strip())
        time.sleep(2)
        
except Exception as e:
    print("Erro no cartão SD:", e)
