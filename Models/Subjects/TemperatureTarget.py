from Interfaces.ISubject import ISubject
from Interfaces.IObserver import IObserver
from typing import List

import RPi.GPIO as GPIO


class TemperatureTarget(ISubject):
    """
    The Temperature target owns the Temp target and hysteresis variable and notifies
    observers (Display and Controller) when these changes.
    """

    _targetTemp: int = 20
    """
    The target temperature set by the user (Default = 20)
    """
    _hysteresis: int = 1

    _observers: List[IObserver] = []
    """
    List of subscribers.
    """
    TEMPTARGET = 0
    HYSTERESIS = 1
    RUNNING = 2
    CONFIRM_STOP = 3
    """
    Program States
    """

    buttonUp = 10
    buttonDown = 22
    buttonOk = 27
    buttonStop = 17

    def __init__(self):
        GPIO.setwarnings(False)  # Ignore warning for now
        GPIO.setmode(GPIO.BCM)  # Use physical GPIO numbering
        GPIO.setup(TemperatureTarget.buttonUp, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(TemperatureTarget.buttonDown, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(TemperatureTarget.buttonOk, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(TemperatureTarget.buttonStop, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(
            TemperatureTarget.buttonUp,
            GPIO.FALLING,
            callback=lambda x: TemperatureTarget.buttonUp_callback(self),
            bouncetime=300,
        )
        GPIO.add_event_detect(
            TemperatureTarget.buttonDown,
            GPIO.FALLING,
            callback=lambda x: TemperatureTarget.buttonDown_callback(self),
            bouncetime=300,
        )
        GPIO.add_event_detect(
            TemperatureTarget.buttonOk,
            GPIO.FALLING,
            callback=lambda x: TemperatureTarget.buttonOk_callback(self),
            bouncetime=300,
        )
        GPIO.add_event_detect(
            TemperatureTarget.buttonStop,
            GPIO.FALLING,
            callback=lambda x: TemperatureTarget.buttonStop_callback(self),
            bouncetime=300,
        )

        self.state = TemperatureTarget.TEMPTARGET

    def attach(self, observer: IObserver) -> None:
        print("Subject: Attached an observer.")
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

        # print("Subject: Notifying observers...")
        for observer in self._observers:
            observer.update(self)

    # --------------------------------------Web Methods-------------------------------------------
    def set_webConfig(self, new_temp: float, new_hysteresis: float) -> None:
        print(f"configured {new_temp} & {new_hysteresis} from web!")
        self._targetTemp = new_temp
        self._hysteresis = new_hysteresis
        self.state = TemperatureTarget.RUNNING
        self.notify()

    def stop_webConfig(self) -> None:
        if self.state == TemperatureTarget.RUNNING:
            print("stopped from web!")
            self.state = TemperatureTarget.TEMPTARGET
            self.notify()

    def get_config(self) -> float:
        return {self._targetTemp, self._hysteresis}

    # --------------------------------------Button Callbacks---------------------------------------
    def buttonUp_callback(channel) -> None:
        print("ButtonUp was pushed!")
        if channel.state == TemperatureTarget.TEMPTARGET:
            channel._targetTemp += 0.5
            channel.notify()

        elif channel.state == TemperatureTarget.HYSTERESIS:
            channel._hysteresis += 0.25
            channel.notify()

    def buttonDown_callback(channel) -> None:
        print("ButtonDown was pushed!")
        if channel.state == TemperatureTarget.TEMPTARGET:
            channel._targetTemp -= 0.5
            channel.notify()

        elif channel.state == TemperatureTarget.HYSTERESIS:
            channel._hysteresis -= 0.25
            channel.notify()

    def buttonOk_callback(channel) -> None:
        print("ButtonOk was pushed!")
        if channel.state == TemperatureTarget.TEMPTARGET:
            channel.state = TemperatureTarget.HYSTERESIS
            channel.notify()

        elif channel.state == TemperatureTarget.HYSTERESIS:
            channel.state = TemperatureTarget.RUNNING
            channel.notify()

        elif channel.state == TemperatureTarget.CONFIRM_STOP:
            channel.state = TemperatureTarget.TEMPTARGET
            channel.notify()

    def buttonStop_callback(channel) -> None:
        print("ButtonStop was pushed!")
        if channel.state == TemperatureTarget.HYSTERESIS:
            channel.state = TemperatureTarget.TEMPTARGET
            channel.notify()

        elif channel.state == TemperatureTarget.RUNNING:
            channel.state = TemperatureTarget.CONFIRM_STOP
            channel.notify()

        elif channel.state == TemperatureTarget.CONFIRM_STOP:
            channel.state = TemperatureTarget.RUNNING
            channel.notify()
