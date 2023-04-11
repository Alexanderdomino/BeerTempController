from Interfaces.IActuator import IActuator

import RPi.GPIO as GPIO

class Heater(IActuator):

    def __init__(self):
        # Set the GPIO mode to BCM numbering
        GPIO.setmode(GPIO.BCM)

        self.heaterGPIO = 9

        # Set GPIO pin as an output
        GPIO.setup(self.heaterGPIO, GPIO.OUT)
        GPIO.output(self.heaterGPIO, GPIO.HIGH)
    
    def Start(self) -> None:
        """
        Sets the GPIO pin high and thereby starts the heater.
        """
        GPIO.output(self.heaterGPIO, GPIO.LOW)

    
    def Stop(self) -> None:
        """
        Sets the GPIO pin low and thereby stops the heater.
        """
        GPIO.output(self.heaterGPIO, GPIO.HIGH)

    def __del__(self):
        """
        Cleans up the GPIO settings when the object is destroyed.
        """
        GPIO.cleanup()