import telebot
import requests
from config import *
from handlers import register_handlers

bot = telebot.TeleBot(BOT_TOKEN)

register_handlers(bot)  # Регистрируем обработчики команд

url = f"https://api.telegram.org/bot{BOT_TOKEN}/setMyCommands"

commands = [
    {"command": "start", "description": "Перезапустить бота"},
    {"command": "menu", "description": "Главное меню"},
    {"command": "aboutus", "description": "О нас"},
    {"command": "info", "description": "Информация о подъемниках"},
    {"command": "contact", "description": "Связаться с нами"},
    {"command": "rent", "description": "Аренда оборудования"},
    {"command": "feedback", "description": "Посмотреть отзывы"},
]

response = requests.post(url, json={"commands": commands})
print(response.json())

if __name__ == "__main__":
    print("Бот запущен")
    bot.infinity_polling()


# timeout=10, long_polling_timeout=5