from machine import Pin, SPI
import os
import time
import sdcard

spi = SPI(
    0,
    baudrate=1_000_000,
    polarity=0,
    phase=0,
    sck=Pin(18),
    mosi=Pin(19),
    miso=Pin(16)
)

cs = Pin(17, Pin.OUT, value=1)

sd = sdcard.SDCard(spi, cs)

os.mount(sd, "/sd")

print("SD montado")
print(os.listdir("/sd"))

# Teste de escrita
with open("/sd/teste.txt", "a") as f:
    f.write("Primeiro teste de escrita\n")

print("Arquivo escrito!")

# Teste de leitura
with open("/sd/20260929.csv", "r") as f:
    print("Conteudo:")
    print(f.read())