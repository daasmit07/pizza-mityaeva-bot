from catalog import PIZZAS, SIZES, DRINKS, make_keyboard
from storage import Storage

class PizzaBot:

    def __init__(self, api, storage: Storage):
        self.api = api
        self.storage = storage

    # Обработка входящих обновлений
    def handle_update(self, update):
        if "message" in update:
            self.handle_message(update["message"])

        elif "callback_query" in update:
            self.handle_callback(update["callback_query"])

    # Начало нового заказа
    def handle_message(self, message):
        chat_id = message["chat"]["id"]
        user_id = message["from"]["id"]

        if message.get("text") == "/start":
            self.storage.save_order(user_id, {
                "step": "pizza"
            })

            self.api.send_message(
                chat_id,
                "Выберите пиццу:",
                make_keyboard(PIZZAS)
            )

    # Обработка выбора пользователя
    def handle_callback(self, callback):
        callback_id = callback["id"]
        user_id = callback["from"]["id"]
        data = callback.get("data")

        message = callback["message"]
        chat_id = message["chat"]["id"]
        message_id = message["message_id"]

        order = self.storage.get_order(user_id)

        if order is None:
            self.api.answer_callback(callback_id)
            return

        keyboard = None
        step = order["step"]

        if step == "pizza" and data in PIZZAS:
            order["pizza"] = data
            order["step"] = "size"

            text = "Выберите размер пиццы:"
            keyboard = make_keyboard(SIZES)

            self.storage.save_order(user_id, order)

        elif step == "size" and data in SIZES:
            order["size"] = data
            order["step"] = "drink"

            text = "Выберите напиток:"
            keyboard = make_keyboard(DRINKS)

            self.storage.save_order(user_id, order)

        elif step == "drink" and data in DRINKS:
            order["drink"] = data

            text = (
                "Ваш заказ оформлен!\n\n"
                f"Пицца: {PIZZAS[order['pizza']]}\n"
                f"Размер: {SIZES[order['size']]}\n"
                f"Напиток: {DRINKS[order['drink']]}"
            )

            self.storage.delete_order(user_id)

        else:
            self.api.answer_callback(callback_id)
            return

        # Подтверждение выбора и переход к следующему шагу
        self.api.answer_callback(callback_id)
        self.api.delete_message(chat_id, message_id)
        self.api.send_message(chat_id, text, keyboard)