# actuators/heater_controller.py

import datetime


class HeaterController:
    def get_season(self):
        month = datetime.datetime.now().month
        if month in [12, 1, 2]:
            return "зима"
        elif month in [3, 4, 5]:
            return "весна"
        elif month in [6, 7, 8]:
            return "лето"
        else:
            return "осень"

    def calculate_heater(self, current_temp):
        """
        current_temp: текущая температура помещения
        Возвращает: команда для обогревателя
        """
        season = self.get_season()

        if season == "зима":
            if current_temp < 24:
                return f"{24}"
            else:
                return "off"

        elif season in ["весна", "осень"]:
            if current_temp < 20:
                return f"{24}"
            elif current_temp > 24:
                return f"off"
            else:
                return "stable"

        else:  # лето
            if current_temp < 24:
                return f"off"
