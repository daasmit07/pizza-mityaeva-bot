
# Telegram-бот заказа пиццы

Домашнее задание №11

Выполнила: Митяева Дарья, группа 3823Б1ФИ2.

## Описание

Telegram-бот позволяет выбрать пиццу, размер и напиток
с помощью inline-клавиатуры.

Получение обновлений осуществляется через long polling.
Незавершённые заказы хранятся в базе данных SQLite
и сохраняются при перезапуске программы.

## Локальный запуск

Необходимо задать переменную окружения TELEGRAM_TOKEN
и выполнить команду:

    python main.py

Переменная TELEGRAM_BASE_URL позволяет указать адрес Bot API.
По умолчанию используется https://api.telegram.org.

## Запуск через Docker

Сборка образа:

    docker build -t pizza-bot .

Запуск контейнера:

    docker run --rm -it --env-file .env -v pizza-data:/app/data -w /app/data pizza-bot python /app/main.py
