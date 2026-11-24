import os
import time

from telegram_api import TelegramAPI
from sqlite_storage import SQLiteStorage
from bot import PizzaBot

def main():
    token = os.getenv("TELEGRAM_TOKEN")

    if not token:
        raise RuntimeError("Не задан TELEGRAM_TOKEN")

    api = TelegramAPI(token)
    storage = SQLiteStorage()
    bot = PizzaBot(api, storage)

    offset = 0

    print("Бот заказа пиццы запущен")

    try:
        # Основной цикл получения обновлений
        while True:
            try:
                updates = api.get_updates(offset)

                for update in updates:
                    bot.handle_update(update)
                    offset = update["update_id"] + 1

            except Exception as error:
                print("Ошибка:", error)
                time.sleep(2)

    except KeyboardInterrupt:
        print("Бот остановлен")

    finally:
        storage.close()


if __name__ == "__main__":
    main()