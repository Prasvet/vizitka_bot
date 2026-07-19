import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from dotenv import load_dotenv
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# --- НАСТРОЙКИ ---
# Сюда мы вставим ID картинки, когда получим его
PHOTO_ID = ""

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# --- КОМАНДЫ ---


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Привет!\n\n"
        "Я бот-визитка. Пока я умею немного, но я быстро учусь.\n"
        "Нажми /help, чтобы узнать подробности."
    )


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "🤖 Справка:\n\n"
        "/start - Начать работу заново\n"
        "/help - Показать это сообщение\n\n"
        "Просто отправь мне любой текст, и я отвечу."
    )


@dp.message(Command("photo"))
async def cmd_photo(message: types.Message):
    if PHOTO_ID == "":
        await message.answer("Сначала отпрафь фото!")
        return

    # Отправляем фото по его ID (мгновенно)
    await message.answer_photo(photo=PHOTO_ID, caption="Вот твое фото! 🚀")


@dp.message(F.photo)
async def get_photo_id(message: types.Message):
    global PHOTO_ID
    # Берем последнее фото (оно самого высокого качества)
    photo_data = message.photo[-1]
    PHOTO_ID = photo_data.file_id

    await message.answer(f"✅ Фото получено!\n\n")


@dp.message(Command("about"))
async def cmd_about(message: types.Message):
    content = (
        "👤 <b>Обо мне</b>\n\n"
        "Я тестовый бот-визитка.\n"
        "Меня создал ученик курса Python.\n\n"
        "<b>Мои контакты:</b>\n"
        "🔥 <a href='https://stepik.org/users/1135389522/profile'>Мой профиль Stepik</a>\n"
        "<i>Напиши мне что-нибудь, и я отвечу эхом!</i>"
    )
    await message.answer(content)


# --- ОБРАБОТКА МЕДИА ---


# Этот хэндлер ругается, если прислали ФАЙЛ, а не картинку
@dp.message(F.document)
async def warning_doc(message: types.Message):
    await message.answer(
        "⚠️ Ты прислал это как файл.\n"
        "Telegram не показывает превью для файлов.\n"
        "Пожалуйста, пришли именно как Фото (сжатое)."
    )


# (Ставим В САМОМ НИЗУ. Если поставить выше, команды сломаются!)
@dp.message()
async def echo_handler(message: types.Message):
    # Проверяем, что пользователь прислал именно текст, а не стикер/фото
    if message.text:
        await message.answer(f"Ты написал: {message.text}")
    else:
        await message.answer("Я понимаю только текст, извини 🤷‍♂️")


# --- ЗАПУСК ---
async def main():
    print("🚀 Бот запущен! (Нажми Ctrl+C для остановки)")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
