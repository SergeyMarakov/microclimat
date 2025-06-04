# bot/telegram_bot.py

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message


class TelegramBot:
    def __init__(self, token, room_state):
        self.bot = Bot(token=token)
        self.dp = Dispatcher()
        self.room_state = room_state

        # Регистрация обработчиков
        self.register_handlers()

    def register_handlers(self):
        @self.dp.message(Command("start"))
        async def start_handler(message: Message):
            await message.answer(
                "👋 Привет!\n"
                "Используйте:\n"
                "/status - текущее состояние\n"
                "/people - количество людей\n"
                "/temperature_in - температура помещения\n"
                "/temperature_out - температура на улице\n"
                "/co2 - уровень CO₂\n"
                "/light - мощность освещения\n"
                "/heater - статус обогревателя\n"
                "/ac - статус кондиционера\n"
                "/ventilation - статус вентиляции"
            )

        @self.dp.message(Command("status"))
        async def status_handler(message: Message):
            data = self.room_state.get_state()
            text = (
                f"📊 Текущее состояние:\n"
                f"🕒 Время: {data['timestamp']}\n"
                f"👥 Количество людей: {data['people_count']}\n"
                f"🌡 Температура помещения: {data['indoor_temp']}°C\n"
                f"🌡 Температура на улице: {data['outdoor_temp']}°C\n"
                f"🫁 Уровень CO₂: {data['co2']} ppm\n"
                f"💡 Освещение: {data['light_power']}\n"
                f"🔥 Обогреватель: {data['heater']}\n"
                f"❄ Кондиционер: {data['ac']}\n"
                f"🌬 Вентиляция: {data['ventilation']}"
            )
            await message.answer(text)

        @self.dp.message(Command("people"))
        async def people_handler(message: Message):
            count = self.room_state.get_state()['people_count']
            await message.answer(f"👥 В помещении: {count} человек(а)")

        @self.dp.message(Command("temperature_in"))
        async def temperature_handler(message: Message):
            temp = self.room_state.get_state()['indoor_temp']
            await message.answer(f"🌡 Температура помещения: {temp}°C")

        @self.dp.message(Command("temperature_out"))
        async def temperature_handler(message: Message):
            temp = self.room_state.get_state()['outdoor_temp']
            await message.answer(f"🌡 Температура на улице: {temp}°C")

        @self.dp.message(Command("co2"))
        async def co2_handler(message: Message):
            co2 = self.room_state.get_state()['co2']
            await message.answer(f"🫁 Уровень CO₂: {co2} ppm")

        @self.dp.message(Command("light"))
        async def light_handler(message: Message):
            light = self.room_state.get_state()['light_power']
            await message.answer(f"💡 Состояние освещения: {light}")

        @self.dp.message(Command("heater"))
        async def heater_handler(message: Message):
            heater = self.room_state.get_state()['heater']
            await message.answer(f"🔥 Состояние обогревателя: {heater}")

        @self.dp.message(Command("ac"))
        async def ac_handler(message: Message):
            ac = self.room_state.get_state()['ac']
            await message.answer(f"❄ Состояние кондиционера: {ac}")

        @self.dp.message(Command("ventilation"))
        async def vent_handler(message: Message):
            vent = self.room_state.get_state()['ventilation']
            await message.answer(f"🌬 Состояние вентиляции: {vent}")

    async def start(self):
        """Запуск бота"""
        print("[BOT] Бот запущен")
        await self.dp.start_polling(self.bot)