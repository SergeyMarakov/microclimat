# actuators/ac_controller.py

import datetime

class ACController:
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

    def calculate_ac(self, current_temp, season=None):
        """
        current_temp: текущая температура помещения
        Возвращает: команда для кондиционера
        """
        season = self.get_season()
        if season == "зима":
            return "off"

        if current_temp > 24:
            return f"{24}"
        else:
            return "off"