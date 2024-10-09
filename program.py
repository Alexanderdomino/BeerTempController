from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from Models.Subjects.TemperatureSensor import TemperatureSensor
from Models.Subjects.TemperatureTarget import TemperatureTarget
from Models.Observers.LCDObserver import LCDObserver
from Models.Observers.TempController import TempController
from Models.Actuators.Heater import Heater
from Models.Actuators.Cooler import Cooler
from Api.routes import get_router
import RPi.GPIO as GPIO
import uvicorn

app = FastAPI()

# Initialize system components
targetConfig = TemperatureTarget()
sensor = TemperatureSensor()
displayManager = LCDObserver()
heater = Heater()
cooler = Cooler()
controller = TempController(heater, cooler)

# Attach observers to the temperature sensor and target config
sensor.attach(displayManager)
targetConfig.attach(displayManager)
sensor.attach(controller)
targetConfig.attach(controller)

# Include routes and inject the targetConfig dependency
app.include_router(get_router(targetConfig))

# Define the scheduler as a global variable
scheduler = AsyncIOScheduler()

@app.on_event("startup")
def startup_event():
    """Start the scheduler when the app starts."""
    scheduler.add_job(sensor.readTemperature, 'interval', seconds=60)
    scheduler.start()

@app.on_event("shutdown")
def shutdown_event():
    """Shut down the scheduler when the app shuts down."""
    scheduler.shutdown()
    GPIO.cleanup()  # Clean up GPIO

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)