## Локальная разработка

1. Клонируйте репозиторий (если нужно) и перейдите в папку проекта:
   bash
   cd vizitka-bot
Создайте файл .env в корне проекта и добавьте туда токен:
env
BOT_TOKEN=ВАШ_ТОКЕН_ОТ_BOTFATHER
Установите зависимости:
bash
uv sync
Запустите бота:
bash
uv run python src/main.py

Деплой на сервер
Клонируйте проект:
bash
git clone <ссылка-на-репозиторий>
cd vizitka-bot
Восстановите окружение:
bash
uv sync
Создайте .env с токеном (вручную, не копируйте с локальной машины):
env
BOT_TOKEN=ВАШ_ТОКЕН_ОТ_BOTFATHER
Запустите:
bash
uv run python src/main.py
Для стабильной работы на сервере используйте systemd, supervisor или контейнер (Docker).