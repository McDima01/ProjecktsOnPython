import requests
from config import BOT_TOKEN

url = f"https://api.telegram.org/bot{BOT_TOKEN}/setMyCommands"
commands = [
    {"command": "start", "description": "Запустить бота"},
    {"command": "help", "description": "Помощь"}
]

response = requests.post(url, json={"commands": commands})
print(response.json())
