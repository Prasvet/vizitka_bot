FROM python:3.12-slim

WORKDIR /app

# Установка curl для uv и базовых утилит
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Установка uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# Копируем только манифесты для предварительного кэширования зависимостей
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Копируем остальной код
COPY . .

# Создаём папку для данных, если вдруг volume не сработает сразу
RUN mkdir -p /app/data

# Запуск
CMD ["uv", "run", "python", "src/main.py"]
