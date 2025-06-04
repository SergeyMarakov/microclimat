# main.py

import asyncio
from sensors.camera import Camera
from sensors.mock_arduino_data_reader import ArduinoDataReader
from actuators.heater_controller import HeaterController
from actuators.ac_controller import ACController
from actuators.light_controller import LightController
from actuators.ventilation_controller import VentilationController
from core.room_state import RoomState
from bot.telegram_bot import TelegramBot

# Инициализация модулей
#camera = Camera(source=r"C:\Users\m3rak\PycharmProjects\microklimat\Видео_без_названия_—_сделано_в_Clipchamp_1.mp4")
camera = Camera(source=0) # камера
sensor_reader = ArduinoDataReader() # или ArduinoDataReader(port='COM3') из sensors.arduino_data_reader
heater_ctrl = HeaterController()
ac_ctrl = ACController()
light_ctrl = LightController()
vent_ctrl = VentilationController()
room_state = RoomState(save_interval_seconds=15)

# Telegram-бот
bot_token = "7548026681:AAHP3SMm_wFu-eHTGSBqu8sWfVO_IiW2F0g"
bot = TelegramBot(bot_token, room_state)


async def system_loop():
    try:
        while True:
            # Получаем количество людей
            # people_count, frame = camera.detect_people()  # без демонстрации
            people_count, frame = camera.show_video_with_boxes()  # с демонстрацией изображения

            if frame is None:
                print("Выход...")
                break

            # Читаем данные с датчиков
            sensor_data = sensor_reader.get_data()

            # Обновляем состояние комнаты
            room_state.update_people(people_count)
            room_state.update_sensors(sensor_data)

            # Принимаем решения по устройствам
            heater_command = heater_ctrl.calculate_heater(sensor_data.get("indoor_temp", 0))
            ac_command = ac_ctrl.calculate_ac(sensor_data.get("indoor_temp", 0))
            light_command = light_ctrl.calculate_light_power(people_count, sensor_data.get("light", 0))
            vent_command = vent_ctrl.calculate_ventilation(sensor_data.get("co2", 0), people_count)

            # Обновляем статус устройств
            room_state.update_actuators({
                "heater": heater_command,
                "ac": ac_command,
                "light_power": light_command,
                "ventilation": vent_command
            })

            # Сохраняем состояние раз в N секунд
            room_state.check_and_save()

            await asyncio.sleep(0.01)

    except KeyboardInterrupt:
        print("Выход...")
    finally:
        camera.release()

async def main():
    bot_task = asyncio.create_task(bot.start())
    system_task = asyncio.create_task(system_loop())

    await asyncio.gather(bot_task, system_task)

if __name__ == "__main__":
    asyncio.run(main())