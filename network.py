import requests
import time

class Minibot:
    def __init__(self, token: str):
        self.token = token
        self.handlers = {}
        self.inline_handlers = {}
        self.offset = None

    def add_handler(self, command: str, handler):
        self.handlers[command] = handler
        print(f"Обработчик для {command} добавлен.")

    def add_inline_handler(self, callback_data: str, handler):
        self.inline_handlers[callback_data] = handler
        print(f"Обработчик для {callback_data} добавлен.")

    def start(self):
        print(f"Bot token: {self.token}")
        while True:
            updates = self.get_updates()
            for update in updates:
                self.handle_update(update)
            time.sleep(1)

    def get_updates(self):
        url = f"https://api.telegram.org/bot{self.token}/getUpdates"
        params = {'timeout': 100, 'offset': self.offset}
        response = requests.get(url, params=params)
        result = response.json()
        if result['ok']:
            updates = result['result']
            if updates:
                self.offset = updates[-1]['update_id'] + 1
            return updates
        return []

    def handle_update(self, update):
        if 'message' in update:
            message = update['message']
            chat_id = message['chat']['id']
            command = message.get('text')
            if command in self.handlers:
                self.handlers[command](chat_id)
        elif 'callback_query' in update:
            callback_query = update['callback_query']
            chat_id = callback_query['message']['chat']['id']
            callback_data = callback_query['data']
            if callback_data in self.inline_handlers:
                self.inline_handlers[callback_data](chat_id)

    def send_message(self, chat_id, text, reply_markup=None):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': text,
        }
        if reply_markup is not None:
            payload['reply_markup'] = reply_markup
        
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"Сообщение отправлено в чат {chat_id}: {text}")
        else:
            print(f"Ошибка отправки сообщения: {response.text}")

    def create_inline_keyboard(self, buttons):
        return {'inline_keyboard': buttons}