# actuators/light_controller.py

class LightController:
    def calculate_light_power(self, people_count, brightness):
        """
        people_count: количество людей в помещении
        brightness: текущая освещённость (люмены)
        Возвращает: мощность освещения или 0
        """
        if people_count <= 0:
            return "off"

        if brightness < 500:
            power = 500 - brightness
            return f"{power}"
        else:
            return "off"