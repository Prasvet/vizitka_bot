import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from dotenv import load_dotenv
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties


# Импортируем типы для кнопок
from aiogram.types import ReplyKeyboardRemove
from keyboards import Btn, get_main_kb


# --- 1. НАСТРОЙКИ ---
MY_NAME = "Михаил Овсянников"
MY_ROLE = "Ученик курса Python"
MY_ABOUT = "Изучаю Go и Python, автоматизирую рутину."

LINK_GITHUB = "https://github.com/Prasvet"
LINK_CHANNEL = ""
LINK_PORTFOLIO = ""

MY_CONTACTS = "Telegram: @Prasvet\nEmail: ovsyannikovm@ya.ru"

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

PHOTO_ID = ""

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


# --- КОМАНДЫ и Кнопки ---


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        f"👋 <strong>Привет!</strong>\n"
        f"Я бот-визитка.\n"
        f"Меня зовут {MY_NAME}. Чем могу помочь?",
        reply_markup=get_main_kb(),
    )


@dp.message(F.text == Btn.ABOUT.value)
@dp.message(Command("about"))
async def show_about(message: types.Message):
    await message.answer(
        f"👤 <strong>{MY_NAME}</strong>\n<em>{MY_ROLE}</em>\n\n{MY_ABOUT}",
        reply_markup=get_main_kb(),
    )


@dp.message(F.text == Btn.PROJECTS.value)
@dp.message(Command("projects"))
async def show_projects(message: types.Message):
    links = []
    if LINK_GITHUB:
        links.append(
            f'• <a href="{LINK_GITHUB}" rel="noopener noreferrer nofollow">GitHub</a>'
        )
    if LINK_CHANNEL:
        links.append(
            f'• <a href="{LINK_CHANNEL}" rel="noopener noreferrer nofollow">Telegram-канал</a>'
        )
    if LINK_PORTFOLIO:
        links.append(
            f'• <a href="{LINK_PORTFOLIO}" rel="noopener noreferrer nofollow">Портфолио</a>'
        )

    if not links:
        await message.answer(
            "У меня пока нет опубликованных проектов.", reply_markup=get_main_kb()
        )
        return

    await message.answer(
        "🧩 <strong>Мои проекты:</strong>\n\n" + "\n".join(links),
        reply_markup=get_main_kb(),
    )


@dp.message(F.text == Btn.CONTACTS.value)
@dp.message(Command("contacts"))
async def show_contacts(message: types.Message):
    await message.answer(
        f"📞 <strong>Свяжитесь со мной:</strong>\n\n{MY_CONTACTS}",
        reply_markup=get_main_kb(),
    )


@dp.message(F.text == "📷 Фото")
@dp.message(Command("photo"))
async def show_photo(message: types.Message):
    if not PHOTO_ID:
        await message.answer(
            "Фото не настроено (вставьте ID в код).", reply_markup=get_main_kb()
        )
        return
    await message.answer_photo(
        photo=PHOTO_ID, caption=f"Это я, {MY_NAME}!", reply_markup=get_main_kb()
    )


@dp.message(F.text == Btn.HIDE.value)
async def btn_hide(message: types.Message):
    await message.answer(
        "Меню спрятано. Напиши /start, чтобы вернуть.",
        reply_markup=ReplyKeyboardRemove(),
    )


# --- ТЕХНИЧЕСКИЕ ХЭНДЛЕРЫ ---


@dp.message(F.photo)
async def get_photo_id(message: types.Message):
    await message.answer(f"ID фото: <code>{message.photo[-1].file_id}</code>")


@dp.message()
async def echo(message: types.Message):
    await message.answer(
        "Я не понимаю. Используй кнопки 👇", reply_markup=get_main_kb()
    )


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
