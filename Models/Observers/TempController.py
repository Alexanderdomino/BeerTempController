from Interfaces.IObserver import IObserver
from Interfaces.ISubject import ISubject
from Interfaces.IActuator import IActuator

from Models.Subjects.TemperatureTarget import TemperatureTarget
from Models.Subjects.TemperatureSensor import TemperatureSensor

class TempController(IObserver):

    _allowedHysteresis: int = 1
    _targetTemp: int = 27

    SETUP = 0
    IDLE = 1
    COOLING = 2
    HEATING = 3

    def __init__(self, heater: IActuator, cooler: IActuator):
        self.state = TempController.SETUP
        self.heater = heater
        self.cooler = cooler

    def update(self, subject: ISubject) -> None:
        if isinstance(subject, TemperatureTarget):
            if subject.state == TemperatureTarget.TEMPTARGET or subject.state == TemperatureTarget.HYSTERESIS:
                self.state = TempController.SETUP
                self.cooler.Stop()
                self.heater.Stop()
            
            elif subject.state == TemperatureTarget.RUNNING:
                self._targetTemp = subject._targetTemp
                self._allowedHysteresis = subject._hysteresis
                self.state = TempController.IDLE
            
        elif isinstance(subject, TemperatureSensor):
            if self.state == TempController.IDLE:
                if subject._currentTemp > (self._targetTemp + self._allowedHysteresis):
                    #implement cooling logic
                    print("Controller: Start cooling")
                    self.cooler.Start()
                    self.state = TempController.COOLING
                
                elif subject._currentTemp < (self._targetTemp - self._allowedHysteresis):
                    #implement heating logic
                    print("Controller: Start heating")
                    self.heater.Start()
                    self.state = TempController.HEATING

            elif self.state == TempController.COOLING:
                if subject._currentTemp > self._targetTemp:
                    #continue cooling
                    print("Controller: Cooling in progress")
                else:
                    #turn off cooling
                    print("Controller: Cooling complete")
                    self.cooler.Stop()
                    self.state = TempController.IDLE

            elif self.state == TempController.HEATING:
                if subject._currentTemp < self._targetTemp:
                    #continue heating
                    print("Controller: Heating in progress")
                else:
                    #turn off heating
                    print("Controller: Heating complete")
                    self.heater.Stop()
                    self.state = TempController.IDLE