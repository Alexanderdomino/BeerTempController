# routes.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from Models.Subjects.TemperatureTarget import TemperatureTarget

# Define the connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

# Instantiate the connection manager
connection_manager = ConnectionManager()

# Define a function to return the router, injecting the TemperatureTarget instance
def get_router(targetConfig: TemperatureTarget):
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
            "hysteresis": settings.hysteresis
        }

    # Route to stop the current run from web
    @router.post("/config/stop")
    def stop_config():
        targetConfig.stop_webConfig()
        return {"message": "Configuration stopped from web"}

    # WebSocket endpoint to connect clients
    @router.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await connection_manager.connect(websocket)
        try:
            while True:
                data = await websocket.receive_text()  # This line could be adjusted based on your needs
                print(f"Received message from client: {data}")  # Handle incoming messages as necessary
        except WebSocketDisconnect:
            connection_manager.disconnect(websocket)
            print("Client disconnected")

    return router
