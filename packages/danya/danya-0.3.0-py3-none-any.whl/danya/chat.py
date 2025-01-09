import requests
from datetime import datetime

BASE_URL = "5.35.46.26:10500"
SEND_URL = f"http://{BASE_URL}//send"
GET_URL = f"http://{BASE_URL}//get"
HEADERS = {"Content-Type": "application/json"}

def send(username, content):
    response = requests.post(SEND_URL, headers=HEADERS, json={"username": username, "content": content})
    if response.status_code == 200:
        msg_id = response.json().get("message_id")
        return msg_id
    print(f"Ошибка при отправке сообщения: {response.text}")
    return None

def hist(last_id=None, n=10):
    payload = {"last_id": last_id} if last_id else {}
    response = requests.post(GET_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        msgs = response.json()
        selected = msgs[-n:] if last_id else msgs
        for msg in selected:
            try:
                ts = datetime.fromisoformat(msg['timestamp']).strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                ts = msg['timestamp']
            print(f"[{ts}] {msg['username']}: {msg['content']}")
        return msgs[-1]['id'] if msgs else last_id
    print(f"Ошибка при получении сообщений: {response.text}")
    return last_id