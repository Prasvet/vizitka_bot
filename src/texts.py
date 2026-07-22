from my_data import NAME, ROLE, LINK_GITHUB, LINK_PORTFOLIO, LINK_TG_CHANNEL
from my_data import SHORT_DESC, CONTACT_EMAIL, CONTACT_TG


def get_home() -> str:
    return (
        f"👋 <strong>Привет!</strong>\n"
        f"Я бот-визитка. Меня зовут {NAME}.\n\n"
        "Выберите раздел в меню 👇"
    )


def get_about() -> str:
    parts = [
        f"👤 <strong>{NAME}</strong>",
        f"<em>{ROLE}</em>\n",
        f"{SHORT_DESC}\n",
        "🔗 <strong>Где меня найти:</strong>",
        # ВАЖНО: f-строки с одинарными внешними кавычками
        f'• <a href="{LINK_GITHUB}" rel="noopener noreferrer nofollow">GitHub</a>',
    ]
    if LINK_TG_CHANNEL:
        parts.append(
            f'• <a href="{LINK_TG_CHANNEL}" rel="noopener noreferrer nofollow">Telegram-канал</a>'
        )

    if LINK_PORTFOLIO:
        parts.append(
            f'• <a href="{LINK_PORTFOLIO}" rel="noopener noreferrer nofollow">Портфолио</a>'
        )

    return "\n".join(parts) + get_footer()


def get_projects() -> str:
    parts = [
        "🧩 <strong>Мои проекты</strong>\n\n",
        "Посмотрите примеры кода и кейсы:\n",
        f'👉 <a href="{LINK_GITHUB}" rel="noopener noreferrer nofollow">Мой GitHub</a>\n',
    ]
    if LINK_PORTFOLIO:
        parts.append(
            f'• <a href="{LINK_PORTFOLIO}" rel="noopener noreferrer nofollow">Портфолио</a>'
        )

    return "\n".join(parts) + get_footer()


def get_contacts() -> str:
    return (
        "📞 <strong>Связь со мной</strong>\n\n"
        f'Telegram: <a href="{CONTACT_TG}" rel="noopener noreferrer nofollow">Написать в личку</a>\n'
        f"Email: <code>{CONTACT_EMAIL}</code>" + get_footer()
    )


def get_footer() -> str:
    return "\n\n<em>Нажмите 🏠 Меню для возврата.</em>"
