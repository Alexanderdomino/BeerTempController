#LIBRARIES
from __future__ import annotations
from time import sleep

from Models.Subjects.TemperatureSensor import TemperatureSensor
from Models.Subjects.TemperatureTarget import TemperatureTarget
from Models.Observers.LCDObserver import LCDObserver
from Models.Observers.TempController import TempController
from Models.Actuators.Heater import Heater
from Models.Actuators.Cooler import Cooler

import RPi.GPIO as GPIO

if __name__ == "__main__":
    try:
        # Init
        targetConfig = TemperatureTarget()
        sensor = TemperatureSensor()
        displayManager = LCDObserver()
        sensor.attach(displayManager)
        targetConfig.attach(displayManager)
        heater = Heater()
        cooler = Cooler()
        controller = TempController(heater, cooler)
        sensor.attach(controller)
        targetConfig.attach(controller)

        while True:
            sensor.readTemperature()
            sleep(60)

    except KeyboardInterrupt:
        # Clean up the GPIO pins
        GPIO.cleanup()