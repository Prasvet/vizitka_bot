## Локальная разработка

1. Клонируйте репозиторий (если нужно) и перейдите в папку проекта:
   bash
   cd vizitka-bot
Создайте файл .env в корне проекта и добавьте туда токен:
TELEGRAM_BOT_TOKEN=ВАШ_ТОКЕН_ОТ_BOTFATHER
Установите зависимости:
bash
uv sync
Запустите бота:
bash
uv run python src/main.py

Деплой на сервер
Вариант 1: Развёртывание через Docker Compose (Рекомендуемый)
Этот вариант лучше всего подходит под твой текущий флоу. Он изолирует зависимости, автоматически перезапускает бота при падении и легко масштабируется.

Требования
Сервер с установленным Docker и Docker Compose.
SSH-доступ под root.
Репозиторий клонирован или распакован в /home/projects/vizitka-bot.
Инструкция
Подготовь окружение:

bash
mkdir -p /home/projects
cd /home/projects
# Если есть git:
git clone git@github.com:Prasvet/vizitka_bot.git
# Или если просто распаковал zip:
# unzip vizitka_bot.zip
cd vizitka_bot
Создай файл .env (обязательно!):
Создай файл с именем .env в папке проекта и добавь туда токен:
TELEGRAM_BOT_TOKEN=ВАШ_ТОКЕН_ОТ_BOTFATHER
⚠️ Важно: Никогда не коммить этот файл в Git! Добавь его в .gitignore.

Запусти бота:
В папке проекта должен лежать docker-compose.yml. Запусти одной командой:

bash
docker compose up -d --build
Флаг --build нужен только при первом запуске или после изменения кода. В дальнейшем достаточно docker compose up -d.

Проверка:

bash
docker ps
docker logs -f vizitka_bot
Пример docker-compose.yml (положи в корень проекта)
yaml
version: '3.8'

services:
  bot:
    build: .
    container_name: vizitka_bot
    restart: unless-stopped
    env_file:
      - .env
    volumes:
      # Сюда будут сохраняться данные (БД, логи), чтобы не пропали при пересоздании контейнера
      - ./data:/app/data
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
Пример Dockerfile (тоже в корне)
dockerfile
FROM python:3.12-slim

WORKDIR /app

# Установка зависимостей через uv
RUN apt-get update && apt-get install -y curl && \
    curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:${PATH}"

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

COPY . .

# Запуск бота
CMD ["uv", "run", "python", "src/main.py"]
Совет для Ansible: Твой плейбук для этого варианта должен просто делать git pull, проверять наличие .env и запускать docker compose up -d. Никаких venv, никаких activate.

