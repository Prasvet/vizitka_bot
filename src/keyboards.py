# Импортируем типы для кнопок
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from enum import Enum


class Btn(Enum):
    "Название кнопок"

    ABOUT = "👤 Обо мне"
    PROJECTS = "🧩 Проекты"
    CONTACTS = "📞 Контакты"
    PHOTO = "📷 Фото"
    HELP = "❓ Помощь"
    HIDE = "❌ Спрятать меню"

    @classmethod
    def values_list(cls):
        """Возвращает список текстовых значений всех кнопок (в порядке объявления)."""
        return [b.value for b in cls]

    @classmethod
    def names_list(cls) -> list[str]:
        """Возвращает список имён кнопок (ABOUT, PHOTO и т.д.)."""
        return [b.name for b in cls]


# Мы создаем функцию, чтобы удобно вызывать меню в любом месте
def get_main_kb() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text=Btn.ABOUT.value), KeyboardButton(text=Btn.PROJECTS.value)],
        [KeyboardButton(text=Btn.CONTACTS.value), KeyboardButton(text=Btn.PHOTO.value)],
        [KeyboardButton(text=Btn.HIDE.value)],
    ]
    return ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите пункт меню...",
    )
