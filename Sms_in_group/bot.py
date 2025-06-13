import requests
import time

TOKEN = 'Тут токен бота'
API_URL = f"https://api.telegram.org/bot{TOKEN}"

def send_message(chat_id, text):
    data = {"chat_id": chat_id, "text": text}
    return requests.post(f"{API_URL}/sendMessage", data=data).json()

def get_updates(offset=None):
    params = {"timeout": 60, "offset": offset}
    return requests.get(f"{API_URL}/getUpdates", params=params).json()

def main():
    print("Бот работает в штатном режиме")
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if updates.get("result"):
            for update in updates["result"]:
                last_update_id = update["update_id"] + 1
                message = update.get("message", {})
                chat_id = message.get("chat", {}).get("id")
                text = message.get("text", "")
                if text.startswith("/sms "):
                    parts = text.split(' ', 2)
                    if len(parts) < 3:
                        send_message(chat_id, "Используй: /sms <group_id> <сообщение>")
                    else:
                        group_id = parts[1]
                        msg = parts[2]
                        resp = send_message(group_id, msg)
                        if resp.get("ok"):
                            send_message(chat_id, "Сообщение отправлено в группу.")
                        else:
                            send_message(chat_id, f"Ошибка: {resp.get('description')}")
        time.sleep(1)

if __name__ == "__main__":
    main()