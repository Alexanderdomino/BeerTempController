#LIBRARIES
from __future__ import annotations
from time import sleep

from Models.Subjects.TemperatureSensor import TemperatureSensor
from Models.Observers.LCDObserver import LCDObserver
from Models.Observers.TempController import TempController

if __name__ == "__main__":

    #Init
    sensor = TemperatureSensor()
    displayManager = LCDObserver()
    sensor.attach(displayManager)
    controller = TempController()
    sensor.attach(controller)

    while True:
        sensor.readTemperature()
        sleep(0.5)
