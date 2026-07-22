import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from dotenv import load_dotenv
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties


# Импортируем типы для кнопок
from keyboards import Btn, get_main_menu, nav_menu

import texts
from my_data import PHOTO_ID, NAME


# --- НАСТРОЙКИ ---

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN не найден! Проверьте файл .env")

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


# --- ХЭНДЛЕРЫ ---


@dp.message(F.text == Btn.MENU.value)
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
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
    print("🚀 Бот запущен! (Нажми Ctrl+C для остановки)")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
