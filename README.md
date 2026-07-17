# vizitka-bot

Бот-визитка на aiogram с эхо-ответом.

## Локальный запуск

1. Создай `.env` в корне проекта:
   ```env
   BOT_TOKEN=
Установи зависимости:
bash
uv sync
Запусти бота:
bash
uv run python src/main.py
Деплой на сервер
bash
git clone <ссылка-на-репозиторий>
cd vizitka-bot
uv sync
# создай .env с токеном вручную на сервере
uv run python src/main.py