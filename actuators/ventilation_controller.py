# actuators/ventilation_controller.py


class VentilationController:
    def calculate_ventilation(self, co2, people_count):
        """
        people_count: количество людей в помещении
        Возвращает: команда для вентиляции, чем число больше тем интенсивнее должна работать вентиляция

        Для офисных помещений (2-й и 3-й классы) оптимальным считается 800–1000 ppm, допустимым — 1000–1400 ppm.
        """

        if people_count:
            if co2 <= 800:
                return "off"
            elif 800 < co2 <= 1400:
                return "800"
            elif 1400 < co2 <= 2000:
                return "1400"
            else:
                return "2000"
        else:
            return "off"


