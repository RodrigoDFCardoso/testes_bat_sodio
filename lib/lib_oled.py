import time
import machine                # Necessário porque o código usa machine.ADC e machine.Pin mais adiante
from machine import PWM, Pin  # PWM, GPIO
from machine import SoftI2C
from ssd1306 import SSD1306_I2C  # OLED 128x64 via I2C
import framebuf

# ------------------------------------------------
#  I2C e OLED
# 
#  - Versões <=V6: SDA=GPIO14, SCL=GPIO15
# ------------------------------------------------
# Dica: se quiser compatibilidade automática, você pode tentar "probar" em 0x3C.
# Aqui mantemos V7 como padrão. Troque os pinos se estiver usando placas anteriores.
i2c = SoftI2C(scl=Pin(15), sda=Pin(14))

oled = SSD1306_I2C(128, 64, i2c)

def update_oled(lines):
    """
    Desenha até 8 linhas (8 px de altura cada) na tela 128x64.
    Espera uma LISTA de strings. Se você passar uma string única,
    o Python vai iterar caractere a caractere (provavelmente indesejado).
    """
    oled.fill(0)
    for i, line in enumerate(lines):
        oled.text(line, 0, i * 8)
    oled.show()


def scroll_text(text, delay=0.05):
    # Adiciona espaços para o texto entrar e sair suavemente
    text = "                " + text + "                "

    for i in range(len(text) - 15):
        oled.fill(0)

        # Mostra 16 caracteres por vez
        oled.text(text[i:i+16], 0, 28)

        oled.show()
        time.sleep(delay)


def update_massages(wifi = '', data = '', update = ''):
    messages = [
        "________________",
        "",
        "   BMS - NaION  ", 
        "________________",
        f" WIFI: {wifi}",
        f" DATA: {data}",
        f" Status: {update}",
        "________________"
    ]

    update_oled(messages)