import sys
import os

print("\n=== ПРОВЕРКА СИСТЕМЫ ===")

# 1) Python
ver = sys.version_info
print(f"✅ Python работает: {ver.major}.{ver.minor}.{ver.micro}")

# 2) .env + токен
env_ok = os.path.exists(".env")
token_ok = False

if env_ok:
    print("✅ Файл .env найден")

    with open(".env", "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    token_line = ""
    for line in lines:
        if line.startswith("BOT_TOKEN="):
            token_line = line
            break

    if not token_line:
        print("❌ В .env нет строки BOT_TOKEN=...")
        print("   👉 Добавьте строку: BOT_TOKEN=ВАШ_ТОКЕН")
    else:
        token_value = token_line.split("=", 1)[1].strip()

        # Простая проверка: токен обычно содержит двоеточие
        if not token_value:
            print("❌ Токен пустой.")
            print("   👉 Вставьте токен из BotFather после BOT_TOKEN=")
        elif ":" not in token_value:
            print("⚠️ Токен выглядит странно (обычно внутри есть двоеточие).")
            print("   👉 Проверьте, что вы скопировали токен полностью.")
        else:
            token_ok = True
            print("✅ Токен в .env выглядит корректно")
else:
    print("❌ Файл .env НЕ НАЙДЕН")
    print("   👉 Создайте файл .env в папке проекта и вставьте токен.")

# 3) aiogram (в этом уроке ещё НЕ обязателен)
try:
    import aiogram  # noqa: F401

    print("✅ Библиотека aiogram: УСТАНОВЛЕНА")
except Exception:
    print("ℹ️ Библиотека aiogram: ЕЩЁ НЕ УСТАНОВЛЕНА (это нормально)")

print("========================")

if env_ok and token_ok:
    print("\n🎉 Отлично! Всё готово к следующему уроку.")
else:
    print("\n⚠️ Есть проблемы. Исправьте их и запустите проверку ещё раз.")
