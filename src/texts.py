from my_data import NAME, ROLE, SHORT_DESC, CONTACT_EMAIL, CONTACT_TG, LINKS, PROJECTS


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
    ]
    for name, link in LINKS.items():
        parts.append(
            f'• <a href="{link}" rel="noopener noreferrer nofollow">{name}</a>'
        )
    return "\n".join(parts) + get_footer()


def get_projects() -> str:
    parts = [
        "🧩 <strong>Мои проекты</strong>\n\n",
        "Посмотрите примеры кода и кейсы:\n",
    ]
    for name, link in PROJECTS.items():
        parts.append(
            f'• <a href="{link}" rel="noopener noreferrer nofollow">{name}</a>'
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
