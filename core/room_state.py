# core/room_state.py

import json
import time


class RoomState:
    def __init__(self, save_interval_seconds=15, filename="state_log.json"):
        """
        :param save_interval_seconds: интервал сохранения в секундах
        :param filename: имя файла для сохранения данных
        """
        self.filename = filename
        self.save_interval = save_interval_seconds
        self.last_save_time = time.time()

        # Состояние системы
        self.state = {
            "timestamp": self._get_timestamp(),
            "people_count": 0,
            "indoor_temp": 0.0,
            "outdoor_temp": 0.0,
            "light": 0,
            "co2": 0,
            "heater": "off",
            "ac": "off",
            "light_power": "off",
            "ventilation": "off"
        }

    def _get_timestamp(self):
        return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())

    def update_people(self, people_count):
        self.state["people_count"] = people_count
        self.update_timestamp()

    def update_sensors(self, sensor_data):
        self.state.update({
            "indoor_temp": sensor_data.get("indoor_temp", self.state["indoor_temp"]),
            "outdoor_temp": sensor_data.get("outdoor_temp", self.state["outdoor_temp"]),
            "light": sensor_data.get("light", self.state["light"]),
            "co2": sensor_data.get("co2", self.state["co2"])
        })
        self.update_timestamp()

    def update_actuators(self, commands):
        for key in ["heater", "ac", "light_power", "ventilation"]:
            if key in commands:
                self.state[key] = commands[key]
        self.update_timestamp()

    def update_timestamp(self):
        self.state["timestamp"] = self._get_timestamp()

    def get_state(self):
        return self.state.copy()

    def check_and_save(self):
        """Проверяет, пора ли сохранять данные"""
        now = time.time()
        if now - self.last_save_time >= self.save_interval:
            self._save_to_json()
            self.last_save_time = now

    def _save_to_json(self):
        with open(self.filename, "a") as f:
            json.dump(self.state, f)
            f.write("\n")
        print(f"[SAVED] Данные сохранены в {self.filename}")
        print(self.state)

    def __str__(self):
        return json.dumps(self.state, indent=2)