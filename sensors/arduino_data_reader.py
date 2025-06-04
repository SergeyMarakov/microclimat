# температура улицы, температура помещения,  освещенность, CO2/
# indoor_temp=24.3,outdoor_temp=22.5,light=600,co2=420

import serial

class ArduinoDataReader:
    def __init__(self, port='COM3', baud_rate=115200):
        """Подключаемся к Arduino"""
        self.serial = serial.Serial(port, baud_rate)

    def get_data(self):
        """Читаем строку и записываем в словарь key=value
        c ардуино прилетает строка --> indoor_temp=24.3,outdoor_temp=22.5,light=600,co2=420"""
        if self.serial.in_waiting > 0:
            line = self.serial.readline().decode('utf-8').strip()
            data = {}

            for pair in line.split(','):
                if '=' in pair:
                    key, value = pair.split('=', 1)
                    key = key.strip()
                    value = value.strip()

                    # Пытаемся преобразовать в число, если возможно
                    try:
                        value = float(value) if '.' in value else int(value)
                    except ValueError:
                        pass

                    data[key] = value

            return data
        return {}