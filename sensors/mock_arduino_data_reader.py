# sensors/mock_arduino_data_reader.py

import random
import time


class ArduinoDataReader:
    def __init__(self, port='COM3', baud_rate=115200):
        """
        Мок-класс для имитации ArduinoDataReader без подключения к реальному порту.
        """
        self.port = port
        self.baud_rate = baud_rate
        print(f"[MOCK] Подключено к виртуальному порту {self.port}")

    def get_data(self):
        """
        Возвращает фиктивные данные, как будто они пришли с Arduino.
        """
        # Имитируем задержку опроса датчика
        time.sleep(0.1)

        return {
            "indoor_temp": round(random.uniform(20.0, 26.0), 1),
            "outdoor_temp": round(random.uniform(10.0, 30.0), 1),
            "light": random.randint(100, 1000),
            "co2": random.randint(400, 2000)
        }