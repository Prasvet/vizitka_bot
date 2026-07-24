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
Этот вариант изолирует зависимости, автоматически перезапускает бота при падении и легко масштабируется.

Требования
Сервер: Ubuntu 24.04 (или совместимая)
Docker CE + Docker Compose v2+
Git
SSH‑доступ с правами root (или sudo)
Примечание: на сервере не требуется установка Python, uv или зависимостей вручную — всё упаковано в Docker‑образ.

Быстрый старт (ручной деплой на чистый сервер)

Если ты хочешь быстро развернуть бота на новом сервере выполни эти шаги по порядку.

1. Подготовка сервера
Убедись, что Docker установлен и запущен:

bash
systemctl status docker
Если Docker не установлен — поставь свежий стек (CE + compose‑плагин):

bash
apt update
apt install -y ca-certificates curl gnupg lsb-release
mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
apt update
apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
systemctl enable docker
systemctl start docker

Проверь версии:

bash
docker --version
docker compose version

2. Создание структуры папок
bash
mkdir -p /home/projects/vizitka_bot
mkdir -p /home/data/vizitka_bot

3. Клонирование репозитория
bash
cd /home/projects/vizitka_bot
git clone https://github.com/Prasvet/vizitka_bot.git .

Примечание: используется HTTPS‑ссылка — не требуется настройка SSH‑ключей на сервере.

4. Настройка переменных окружения
Создай файл .env с токеном бота:

bash
cat > .env <<EOF
TELEGRAM_BOT_TOKEN=твой_токен_для_сервера
EOF
chmod 600 .env

Никогда не коммить .env в Git. Файл уже добавлен в .gitignore.

5. Запуск бота
bash
docker compose build
docker compose up -d

Проверка статуса:

bash
docker compose ps

Просмотр логов (используй имя сервиса bot, а не имя контейнера):

bash
docker compose logs --tail=50 bot

6. Проверка работы
Напиши боту в Telegram. Если он отвечает — деплой успешен.

Для теста автоперезапуска:

bash
docker kill vizitka_bot
sleep 15
docker compose ps

Контейнер должен подняться автоматически (благодаря restart: unless-stopped).

Деплой через Ansible
Если ты используешь Ansible для автоматизации, вот готовый плейбук, который делает всё то же самое, что и ручной деплой.

Плейбук deploy-vizitka.yml
yaml
---
- name: Deploy vizitka_bot on server
  hosts: vizitka
  become: yes
  vars:
    project_path: /home/projects/vizitka_bot
    data_path: /home/data/vizitka_bot
    telegram_token: "{{ telegram_token }}"

  tasks:
    - name: Ensure project and data directories exist
      ansible.builtin.file:
        path: "{{ item }}"
        state: directory
        mode: "0755"
      loop:
        - "{{ project_path }}"
        - "{{ data_path }}"

    - name: Clone vizitka_bot repository
      ansible.builtin.git:
        repo: "https://github.com/Prasvet/vizitka_bot.git"
        dest: "{{ project_path }}"
        force: yes
        accept_hostkey: yes

    - name: Create .env with token
      ansible.builtin.copy:
        content: |
          TELEGRAM_BOT_TOKEN={{ telegram_token }}
        dest: "{{ project_path }}/.env"
        mode: "0600"
        owner: root
        group: root

    - name: Build and start the bot
      community.docker.docker_compose:
        project_src: "{{ project_path }}"
        state: present
        pull: yes
        build: yes
        restarted: false
        stopped: false

    - name: Disable old systemd service (если был)
      ansible.builtin.systemd:
        name: vizitka_bot
        enabled: no
        state: stopped
        daemon_reload: yes
Запуск:

bash
ansible-playbook deploy-vizitka.yml --extra-vars "telegram_token=твой_токен"
Важные нюансы
Конфликт экземпляров. Telegram не позволяет делать getUpdates одновременно с двух мест для одного бота. Если ты раньше запускал бота через systemd — обязательно отключи его (systemctl disable && systemctl stop), иначе получишь TelegramConflictError.
Имя сервиса vs имя контейнера. В docker compose команды вроде logs, restart используют имя сервиса (в этом проекте это bot), а не container_name. Правильно: docker compose logs bot.
.idea/ и другие IDE‑файлы. Они добавлены в .gitignore и не должны попадать в репозиторий и на сервер.
uv и зависимости. Все зависимости фиксируются в uv.lock, сборка происходит внутри Docker. На сервере не нужно ставить uv или Python.

Хранение данных. Данные бота сохраняются в томе /home/data/vizitka_bot:/app/data — они не пропадут при пересборке образа.

Полезные команды
bash
# Статус контейнеров
docker compose ps

# Логи бота
docker compose logs --tail=100 bot

# Перезапуск
docker compose restart

# Полная остановка и удаление контейнеров (не трогает тома)
docker compose down

# Очистка образов (если нужно освободить место)
docker image prune -f
Лицензия и контакты
Лицензия: MIT (или укажи свою).
Автор: Prasvet.
Репозиторий: git@github.com:Prasvet/vizitka_bot.git.

Как внести вклад
Сделай fork репозитория.
Создай ветку: git checkout -b feature/name.
Внеси изменения, сделай коммит.
Отправь PR.
Перед коммитом убедись, что:

.env не попал в Git.
Нет лишних IDE‑файлов (.idea/, .vscode/, __pycache__).
Зависимости зафиксированы в uv.lock.
Для разработчиков (локально)
Локальная разработка ведётся в виртуальном окружении с uv. Пример:

bash
uv venv
source .venv/bin/activate
uv sync --no-dev
uv run python src/main.py bot

Docker используется только для деплоя и CI/CD.

