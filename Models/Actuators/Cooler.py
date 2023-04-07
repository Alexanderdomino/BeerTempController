from Interfaces.IActuator import IActuator

import RPi.GPIO as GPIO

class Cooler(IActuator):

    def __init__(self):
        # Set the GPIO mode to BCM numbering
        GPIO.setmode(GPIO.BCM)

        self.coolerGPIO = 11

        # Set GPIO pin as an output
        GPIO.setup(self.coolerGPIO, GPIO.OUT)
        GPIO.output(self.coolerGPIO, GPIO.LOW)
    
    def Start(self) -> None:
        """
        Sets the GPIO pin high and thereby starts the cooler.
        """
        GPIO.output(self.coolerGPIO, GPIO.HIGH)

    
    def Stop(self) -> None:
        """
        Sets the GPIO pin low and thereby stops the cooler.
        """
        GPIO.output(self.coolerGPIO, GPIO.LOW)

    def __del__(self):
        """
        Cleans up the GPIO settings when the object is destroyed.
        """
        GPIO.cleanup()