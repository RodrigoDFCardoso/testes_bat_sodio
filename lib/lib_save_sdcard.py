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


def salvar_dados(dados):
    # dados:
    # [timestamp, channel, temperature, voltage, current, power]
    #print(dados)

    timestamp = dados[0]

    # Converte o timestamp para data
    data = time.localtime(timestamp)

    # Nome: YYYYMMDD.csv
    nome_arquivo = "/sd/{:04d}{:02d}{:02d}.csv".format(
        data[0],
        data[1],
        data[2]
    )

    # Verifica se o arquivo existe
    existe = nome_arquivo in os.listdir("/sd")

    # Abre para adicionar
    with open(nome_arquivo, "a") as arquivo:
        dado = f'{int(dados[0])};{str(dados[1])};{float(dados[2])};{float(dados[3])};{float(dados[4])};{float(dados[5])}'
        print(dado)
        # Grava os dados
        arquivo.write(
            dado + "\n"
        )
        
        print("sdcard gravado")
        


