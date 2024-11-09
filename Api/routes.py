# routes.py
from fastapi import APIRouter
from pydantic import BaseModel
from Models.Subjects.TemperatureTarget import TemperatureTarget
from Models.Observers.SaveTempObserver import SaveTempObserver


# Define a function to return the router, injecting the TemperatureTarget instance
def get_router(targetConfig: TemperatureTarget, tempData: SaveTempObserver):
    router = APIRouter()

    # Pydantic model for temperature and hysteresis configuration
    class TempConfigModel(BaseModel):
        target_temperature: float
        hysteresis: float

    # Route to get the current temperature and hysteresis configuration
    @router.get("/config")
    def get_config():
        config = targetConfig.get_config()
        return config

    # Route to set new temperature and hysteresis from web
    @router.post("/config")
    def set_config(settings: TempConfigModel):
        targetConfig.set_webConfig(settings.target_temperature, settings.hysteresis)
        return {
            "message": "Configuration set from web",
            "target_temperature": settings.target_temperature,
            "hysteresis": settings.hysteresis,
        }

    # Route to stop the current run from web
    @router.get("/config/stop")
    def stop_config():
        targetConfig.stop_webConfig()
        return {"message": "Configuration stopped from web"}

    @router.get("/temp-readings")
    def get_temp_readings():
        return tempData.get_temperatures()

    return router
