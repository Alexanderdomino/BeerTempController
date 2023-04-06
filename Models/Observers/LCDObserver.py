import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

from Interfaces.IObserver import IObserver
from Interfaces.ISubject import ISubject

targetTemp = 27.00

# Defintion of LCDObserver class, which is a subclass of Observer
class LCDObserver(IObserver):

    """--------------------------------------Display Setup---------------------------------------"""
    # LCD size
    lcd_columns = 16
    lcd_rows = 2

    # GPIO setup
    lcd_rs = digitalio.DigitalInOut(board.D23)
    lcd_en = digitalio.DigitalInOut(board.D11)
    lcd_d7 = digitalio.DigitalInOut(board.D27)
    lcd_d6 = digitalio.DigitalInOut(board.D22)
    lcd_d5 = digitalio.DigitalInOut(board.D10)
    lcd_d4 = digitalio.DigitalInOut(board.D9)

    # Definition of object
    lcd = characterlcd.Character_LCD_Mono(
        lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows
    )

    lcd.clear()
    # Define the custom character for the degree symbol
    degree_char = bytes([0x02,0x05,0x02,0x00,0x00,0x00,0x00,0x00])

    lcd.create_char(1, degree_char)

    def update(self, subject: ISubject) -> None:
        self.lcd.message = "Temp:    %.2f%cC\nTarget:  %.2f%cC" % (subject._currentTemp, 1, targetTemp, 1)
