from dataclasses import dataclass

from aiogram.types import ReplyKeyboardMarkup

from models.models import *

KEYBOARDS = {
    "ENG": [
        ["👤My profile"],
        ["💣Attack number"]
    ],
    "RU": [
        ["👤Мой профиль"],
        ["💣Атаковать номер"]
    ]
}

TEXT = {
    "type": {
        "start": {
            "ENG": "🤖UBI is BOT\n Help - /help",
            "RU": "🤖UBI Бот\n Помощь - /help"
        },
        "attack": {
            "circles": {
                "ENG": "Received 30 circles for attack.",
                "RU": "Получено 30 кругов для атаки."
            },
            "phone": {
                "ENG": "/cancel - Cancel\nEnter phone number:",
                "RU": "/cancel - Отменить\nВведите номер телефона:"
            },
        },
        "change_language": {
            "ENG": "🌐Select the language",
            "RU": "🌐Выберите язык"
        },
        "cancel": {
            "ENG": "Canceled",
            "RU": "Отменено"
        },
        "correct_phone": {
            "ENG": "You only need to enter numbers\n/cancel - Отменить",
            "RU": "Нужно вводить только цифры\n/cancel - Отменить"
        },
        "stop_attack": {
            "ENG": "Stop the attack?",
            "RU": "Остановить атаку?"
        }
    }
}

@dataclass
class Language:
    user_id: int
    symbol: str

    def __init__(self, user_id="", symbol=""):
        self.user_id = user_id
        self.symbol = symbol

    async def update(self):
        user_data = await UserData.objects.get(username=self.user_id)
        await user_data.update(language=self.symbol)

    def text(self, type):
        return TEXT["type"][type][self.symbol]
    
    def set_circles_text(self, type=""):
        return TEXT["type"]["attack"]["circles"][self.symbol]

    def set_phone_text(self, type=""):
        return TEXT["type"]["attack"]["phone"][self.symbol]

    def keyboard(self, symbol=""):
        if self.symbol:
            return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=KEYBOARDS[self.symbol])
        elif symbol:
            return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=KEYBOARDS[symbol])
        else:
            return None

    def extend_keyboards(self):
        keyboard = KEYBOARDS["ENG"][:]
        keyboard.extend(KEYBOARDS["RU"])
        return keyboard