import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

from Interfaces.IObserver import IObserver
from Interfaces.ISubject import ISubject

from Models.Subjects.TemperatureTarget import TemperatureTarget
from Models.Subjects.TemperatureSensor import TemperatureSensor


# Defintion of LCDObserver class, which is a subclass of Observer
class LCDObserver(IObserver):

    _currentTemp: int = 0
    _targetTemp: int = 0
    _hysteresis: int = 0

    SETUP = 0
    RUNNING = 1

    """--------------------------------------Display Setup---------------------------------------"""
    _backlightTimer: int = 2

    # LCD size
    lcd_columns = 16
    lcd_rows = 2

    def __init__(self):
        self.reinitialize_lcd()
        self.state = LCDObserver.SETUP
        self.lcd.message = "   Welcome HJ   \nPress Any Button"

    def reinitialize_lcd(self):
        # Clean up the previous LCD instance if it exists
        if hasattr(self, 'lcd'):
            del self.lcd

        # GPIO setup
        lcd_rs = digitalio.DigitalInOut(board.D26)
        lcd_en = digitalio.DigitalInOut(board.D19)
        lcd_d7 = digitalio.DigitalInOut(board.D0)
        lcd_d6 = digitalio.DigitalInOut(board.D5)
        lcd_d5 = digitalio.DigitalInOut(board.D6)
        lcd_d4 = digitalio.DigitalInOut(board.D13)

        # Definition of object
        self.lcd = characterlcd.Character_LCD_Mono(
            lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, self.lcd_columns, self.lcd_rows
        )

        # Define the custom character for the degree symbol
        degree_char = bytes([0x02, 0x05, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00])
        self.lcd.create_char(1, degree_char)

    def update(self, subject: ISubject) -> None:
        if isinstance(subject, TemperatureTarget):
            if subject.state == TemperatureTarget.TEMPTARGET:
                self._targetTemp = subject._targetTemp
                self.reinitialize_lcd()
                self.lcd.message = " Select Target: \n     %.2f%cC    " % (self._targetTemp, 1)
                self.state = LCDObserver.SETUP
            
            elif subject.state == TemperatureTarget.HYSTERESIS:
                self._hysteresis = subject._hysteresis
                self.reinitialize_lcd()
                self.lcd.message = "  Hysteresis:   \n     %.2f%cC    " % (self._hysteresis, 1)
                self.state = LCDObserver.SETUP
            
            elif subject.state == TemperatureTarget.RUNNING:
                self.reinitialize_lcd()
                self.lcd.message = " Wait for first \n Measurement... "
                self.state = LCDObserver.RUNNING
                self._backlightTimer = 2


        elif isinstance(subject, TemperatureSensor):
            if self.state == LCDObserver.RUNNING:
                self._currentTemp = subject._currentTemp
                self.reinitialize_lcd()
                self.lcd.message = "Temp:    %.2f%cC\nTarget:  %.2f%cC" % (self._currentTemp, 1, self._targetTemp, 1)
                if self._backlightTimer < 1:
                    # turn off backlight
                else:
                    self._backlightTimer -= 1