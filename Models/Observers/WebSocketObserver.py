# WebSocketObserver.py
from Interfaces.IObserver import IObserver
from Api.routes import connection_manager  # Ensure you have access to your connection manager
import asyncio  # Import asyncio

class WebSocketObserver(IObserver):
    def update(self, subject):
        # This method will be called when the subject (TemperatureSensor) notifies its observers
        temperature = subject.get_temperature()  # Assuming you have a method to get the current temperature
        message = f"New temperature: {temperature}"
        asyncio.create_task(connection_manager.send_message(message))  # Send message asynchronously
