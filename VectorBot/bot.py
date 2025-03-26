import telebot
import requests
from config import *
from handlers import register_handlers


bot = telebot.TeleBot(BOT_TOKEN)

register_handlers(bot)  # Регистрируем обработчики команд

url = f"https://api.telegram.org/bot{BOT_TOKEN}/setMyCommands"
commands = [
    {"command": "start", "description": "Перезапустить бота"},
    {"command": "settings", "description": "настройка бота"},
    {"command": "post", "description": "Принудительно запостить музыку"},
    {"command": "start_auto", "description": "Начать \"автопост\" музыки "},
    {"command": "stop_auto", "description": "Прекратить \"автопост\" музыки"},
    {"command": "download", "description": "Скачать трек по ссылке"}
]

response = requests.post(url, json={"commands": commands})
print(response.json())

if __name__ == "__main__":
    print("Бот запущен")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)


