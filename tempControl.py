#tempControl.py

#LIBRARIES
from __future__ import annotations
from abc import ABC, abstractmethod
from random import randrange
from typing import List
from time import sleep

#LIBRARIES RPI
from w1thermsensor import W1ThermSensor, Unit
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

"""-------------------------------------Global variables-------------------------------------"""

targetTemp = 20
allowedHysteresis = 1

"""--------------------------------------Observer Pattern------------------------------------"""

"""------------------------------Subjects----------------------------"""
# Define the Subject Interface
class Subject(ABC):

    @abstractmethod
    def attach(self, observer: Observer) -> None:
        """
        Attach an observer to the subject.
        """
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        """
        Detach an observer from the subject.
        """
        pass

    @abstractmethod
    def notify(self) -> None:
        """
        Notify all observers about an event.
        """
        pass

# Define the Concrete Subject
class TemperatureSensor(Subject):
    """
    The Temperature sensor owns the currentTemp variable and notifies
    observers (Display and Controller) when the temperature changes.
    """
    tempSensor = W1ThermSensor()
    """
    init of sensor
    """

    _currentTemp: int = None
    """
    The Current temperature read by the sensor (Default = 0)
    """

    _observers: List[Observer] = []
    """
    List of subscribers.
    """

    def attach(self, observer: Observer) -> None:
        print("Subject: Attached an observer.")
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    """
    The subscription management methods.
    """

    def notify(self) -> None:
        """
        Trigger an update in each subscriber.
        """

        print("Subject: Notifying observers...")
        for observer in self._observers:
            observer.update(self)

    def readTemperature(self) -> None:
        """
        Reads the current temperature and notifies observers of about the new reading.
        """

        print("\nSubject: Reading temperature.")
        self._currentTemp = self.tempSensor.get_temperature()

        print(f"Subject: Current Temperature is changed to: {self._currentTemp}")
        self.notify()


"""------------------------------Observers----------------------------"""

class Observer(ABC):
    """
    The Observer interface declares the update method, used by subjects.
    """

    @abstractmethod
    def update(self, subject: Subject) -> None:
        """
        Receive update from subject.
        """
        pass

# Define the LCDObserver class, which is a subclass of Observer
class LCDObserver(Observer):

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
    def update(self, subject: Subject) -> None:
        self.lcd.message = "Temp:    %.2f C\nTarget:  20.00 C" % (subject._currentTemp)


"""---------------------------------------Program Start--------------------------------------"""

if __name__ == "__main__":

    #Init
    sensor = TemperatureSensor()
    displayManager = LCDObserver()
    sensor.attach(displayManager)

    while True:
        sensor.readTemperature()
        sleep(0.5)
