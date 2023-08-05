from Interfaces.ISubject import ISubject
from Interfaces.IObserver import IObserver
from typing import List

from w1thermsensor import W1ThermSensor, Unit

class TemperatureSensor(ISubject):
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
    The Current temperature read by the sensor (Default = None)
    """

    _observers: List[IObserver] = []
    """
    List of subscribers.
    """

    def attach(self, observer: IObserver) -> None:
        self._observers.append(observer)

    def detach(self, observer: IObserver) -> None:
        self._observers.remove(observer)

    """
    The subscription management methods.
    """

    def notify(self) -> None:
        """
        Trigger an update in each subscriber.
        """

        #print("Subject: Notifying observers...")
        for observer in self._observers:
            observer.update(self)

    def readTemperature(self) -> None:
        """
        Reads the current temperature and notifies observers of about the new reading.
        """
        tmp_temp = self.tempSensor.get_temperature()

        if 1 < tmp_temp < 50:
            self._currentTemp = tmp_temp
            self.notify()
