import collections
import csv
import os
from datetime import datetime
from Interfaces.IObserver import IObserver
from Interfaces.ISubject import ISubject
from Models.Subjects.TemperatureSensor import TemperatureSensor


class SaveTempObserver(IObserver):
    MAX_SIZE = 20160  # 2 weeks of data at 1-minute intervals
    FILE_PATH = "temperature_data.csv"

    def __init__(self):
        self.temperatures = collections.deque(maxlen=self.MAX_SIZE)
        self.load_from_file()

    def update(self, subject: ISubject) -> None:
        if isinstance(subject, TemperatureSensor):
            timestamp = datetime.now().isoformat()
            temperature = subject._currentTemp
            self.temperatures.append(
                {"timestamp": timestamp, "temperature": temperature}
            )
            self.append_to_file(timestamp, temperature)

    def get_temperatures(self):
        return list(self.temperatures)

    def append_to_file(self, timestamp, temperature):
        file_exists = os.path.isfile(self.FILE_PATH)
        with open(self.FILE_PATH, "a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(
                    ["timestamp", "temperature"]
                )  # Write header if file is new
            writer.writerow([timestamp, temperature])

    def load_from_file(self):
        if os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, "r") as file:
                reader = csv.DictReader(file)
                data = list(reader)
                self.temperatures = collections.deque(data, maxlen=self.MAX_SIZE)
