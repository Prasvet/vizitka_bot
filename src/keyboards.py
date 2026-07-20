# Импортируем типы для кнопок
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from enum import Enum


class Btn(Enum):
    "Название кнопок"

    ABOUT = "👤 Обо мне"
    PHOTO = "📷 Фото"
    HELP = "❓ Помощь"
    HIDE = "❌ Спрятать меню"


# Мы создаем функцию, чтобы удобно вызывать меню в любом месте
def get_main_kb() -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text=Btn.ABOUT.value),
            KeyboardButton(text=Btn.PHOTO.value),
        ],
        [
            KeyboardButton(text=Btn.HELP.value),
            KeyboardButton(text=Btn.HIDE.value),
        ],
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
