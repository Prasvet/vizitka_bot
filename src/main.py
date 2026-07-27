import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from dotenv import load_dotenv

import texts

# Импортируем типы для кнопок
from keyboards import Btn, get_main_menu, nav_menu
from my_data import NAME, PHOTO_ID

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


# --- НАСТРОЙКИ ---

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не найден! Проверьте файл .env")
else:
    logger.info("✅ Токен успешно загружен")

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


# --- ХЭНДЛЕРЫ ---


@dp.message(F.text == Btn.MENU.value)
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    logger.info(f"📩 Получен /start от пользователя {message.from_user.id}")
    await message.answer(texts.get_home(), reply_markup=get_main_menu())


@dp.message(F.text == Btn.ABOUT.value)
@dp.message(Command("about"))
async def show_about(message: types.Message):
    await message.answer(texts.get_about(), reply_markup=nav_menu())


@dp.message(F.text == Btn.PROJECTS.value)
@dp.message(Command("projects"))
async def show_projects(message: types.Message):
    await message.answer(texts.get_projects(), reply_markup=nav_menu())


@dp.message(F.text == Btn.CONTACTS.value)
@dp.message(Command("contacts"))
async def show_contacts(message: types.Message):
    await message.answer(texts.get_contacts(), reply_markup=nav_menu())


@dp.message(F.text == "📷 Фото")
@dp.message(Command("photo"))
async def show_photo(message: types.Message):
    if not PHOTO_ID:
        await message.answer(
            "Фото не настроено (вставьте ID в код).",
            reply_markup=nav_menu(),
        )
        return
    await message.answer_photo(
        photo=PHOTO_ID, caption=f"Это я, {NAME}!", reply_markup=nav_menu()
    )


@dp.message(F.text == Btn.HIDE.value)
async def btn_hide(message: types.Message):
    await message.answer(
        "Меню спрятано. Напиши /start, чтобы вернуть.",
        reply_markup=nav_menu(),
    )


# --- ТЕХНИЧЕСКИЕ ХЭНДЛЕРЫ ---


@dp.message(F.photo)
async def get_photo_id(message: types.Message):
    await message.answer(f"ID фото: <code>{message.photo[-1].file_id}</code>")


@dp.message()
async def fallback_handler(message: types.Message):
    content = "\n".join(
        "Я пока не понимаю такие сообщения 🙂",
        "Пожалуйста, используйте кнопки меню.",
    )
    await message.answer(content, reply_markup=nav_menu())


# Этот хэндлер ругается, если прислали ФАЙЛ, а не картинку
@dp.message(F.document)
async def warning_doc(message: types.Message):
    await message.answer(
        "⚠️ Ты прислал это как файл.\n"
        "Telegram не показывает превью для файлов.\n"
        "Пожалуйста, пришли именно как Фото (сжатое)."
    )


# --- ЗАПУСК ---
async def main():
    logger.info("🚀 Запуск бота Vizitka...")
    print("🚀 Бот запущен! (Нажми Ctrl+C для остановки)")
    await dp.start_polling(bot)
    logger.info("🛑 Бот остановлен")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
