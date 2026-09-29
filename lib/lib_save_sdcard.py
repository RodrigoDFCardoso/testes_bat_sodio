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


def salvar_dados(dados):
    # dados:
    # [timestamp, channel, temperature, voltage, current, power]

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

        # Grava os dados
        arquivo.write(
            ";".join(str(valor) for valor in dados) + "\n"
        )
        


