FROM python:3.12-slim

# Устанавливаем uv (он нужен для установки зависимостей внутри образа)
RUN pip install --no-cache-dir uv

WORKDIR /app

# Копируем только файлы описания проекта сначала (чтобы кэш слоёв работал быстрее)
COPY pyproject.toml uv.lock ./

# Синхронизируем зависимости (uv возьмёт версии строго из uv.lock)
RUN uv sync --frozen

# Теперь копируем весь остальной код
COPY . .

# Команда запуска: uv sync уже был, теперь просто стартуем бота
CMD ["uv", "run", "python", "src/main.py"]
