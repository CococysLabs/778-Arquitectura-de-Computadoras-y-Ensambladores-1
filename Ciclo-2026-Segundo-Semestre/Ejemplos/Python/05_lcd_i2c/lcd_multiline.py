import time
from rpi_lcd import LCD

lcd = LCD(0x27, 1, 16, 2, True)
message = "Texto largo que se reparte en las dos lineas del LCD I2C"

try:
    lcd.text(message, 1)
    time.sleep(10)
finally:
    try:
        lcd.clear()
    finally:
        lcd.bus.close()
