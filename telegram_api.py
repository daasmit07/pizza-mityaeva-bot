import os
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError

class TelegramAPI:

    def __init__(self, token):
        base_url = os.getenv(
            "TELEGRAM_BASE_URL",
            "https://api.telegram.org"
        ).rstrip("/")

        self.url = f"{base_url}/bot{token}/"

    # Запрос к Telegram Bot API
    def request(self, method, data=None):
        body = json.dumps(data or {}).encode("utf-8")

        request = Request(
            self.url + method,
            data=body,
            headers={"Content-Type": "application/json"}
        )

        try:
            with urlopen(request, timeout=60) as response:
                return json.loads(response.read())["result"]

        except HTTPError as error:
            details = json.loads(error.read())
            description = details.get(
                "description",
                "Неизвестная ошибка"
            )

            raise RuntimeError(
                f"{method}: {error.code} - {description}"
            ) from None

    # Получение обновлений через long polling
    def get_updates(self, offset=0):
        return self.request("getUpdates", {
            "offset": offset,
            "timeout": 30,
            "limit": 100,
            "allowed_updates": ["message", "callback_query"]
        })

    # Отправка сообщения
    def send_message(self, chat_id, text, keyboard=None):
        data = {
            "chat_id": chat_id,
            "text": text
        }

        if keyboard is not None:
            data["reply_markup"] = keyboard

        return self.request("sendMessage", data)

    # Удаление предыдущего сообщения
    def delete_message(self, chat_id, message_id):
        return self.request("deleteMessage", {
            "chat_id": chat_id,
            "message_id": message_id
        })

    # Подтверждение нажатия кнопки
    def answer_callback(self, callback_id):
        try:
            return self.request("answerCallbackQuery", {
                "callback_query_id": callback_id
            })

        except RuntimeError as error:
            if "query is too old" in str(error):
                return None

            raise