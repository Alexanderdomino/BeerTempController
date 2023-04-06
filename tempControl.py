#tempControl.py

#LIBRARIES
from __future__ import annotations
from abc import ABC, abstractmethod
from random import randrange
from typing import List
from time import sleep

#LIBRARIES RPI
from w1thermsensor import W1ThermSensor, Unit

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

# Define the LCDObserver class, which is a subclass of Observer
class LCDObserver(Observer):

    def update(self, subject: Subject) -> None:
        print(f"Writing to the LCD Display: {subject._currentTemp}")


class TempController(Observer):

    def update(self, subject: Subject) -> None:
        print(f"Writing to the LCD Display: {subject._currentTemp}")


"""---------------------------------------Program Start--------------------------------------"""

if __name__ == "__main__":

    #Init
    sensor = TemperatureSensor()
    displayManager = LCDObserver()
    sensor.attach(displayManager)

    #Testing
    sensor.readTemperature()
    sleep(5)
    sensor.readTemperature()
    sleep(5)
    sensor.readTemperature()
