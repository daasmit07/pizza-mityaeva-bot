import sqlite3
import json

from storage import Storage


class SQLiteStorage(Storage):

    def __init__(self, db_path="orders.db"):
        self.connection = sqlite3.connect(db_path)

        # Создание таблицы заказов
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                user_id INTEGER PRIMARY KEY,
                order_data TEXT NOT NULL
            )
        """)
        self.connection.commit()

    # Получение заказа пользователя
    def get_order(self, user_id):
        cursor = self.connection.execute(
            "SELECT order_data FROM orders WHERE user_id = ?",
            (user_id,)
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return json.loads(row[0])

    # Сохранение или обновление заказа
    def save_order(self, user_id, order):
        self.connection.execute("""
            INSERT OR REPLACE INTO orders (user_id, order_data)
            VALUES (?, ?)
        """, (user_id, json.dumps(order)))

        self.connection.commit()

    # Удаление заказа
    def delete_order(self, user_id):
        self.connection.execute(
            "DELETE FROM orders WHERE user_id = ?",
            (user_id,)
        )
        self.connection.commit()

    def close(self):
        self.connection.close()