from Interfaces.IObserver import IObserver
from Interfaces.ISubject import ISubject

allowedHysteresis = 1
targetTemp = 27.00

class TempController(IObserver):

    IDLE = 0
    COOLING = 1
    HEATING = 2

    def __init__(self):
        self.state = TempController.IDLE

    def update(self, subject: ISubject) -> None:
        if self.state == TempController.IDLE:
            if subject._currentTemp > (targetTemp + allowedHysteresis):
                #implement cooling logic
                print("Controller: Start cooling")
                self.state = TempController.COOLING
            
            elif subject._currentTemp < (targetTemp - allowedHysteresis):
                #implement heating logic
                print("Controller: Start heating")
                self.state = TempController.HEATING

        elif self.state == TempController.COOLING:
            if subject._currentTemp > targetTemp:
                #continue cooling
                print("Controller: Cooling in progress")
            else:
                #turn off cooling
                print("Controller: Cooling complete")
                self.state = TempController.IDLE

        elif self.state == TempController.HEATING:
            if subject._currentTemp < targetTemp:
                #continue heating
                print("Controller: Heating in progress")
            else:
                #turn off heating
                print("Controller: Heating complete")
                self.state = TempController.IDLE