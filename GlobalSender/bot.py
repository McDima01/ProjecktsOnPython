import telebot
import requests
from config import BOT_TOKEN
from handlers import register_handlers

bot = telebot.TeleBot(BOT_TOKEN)

register_handlers(bot)  # Регистрируем обработчики команд


url = f"https://api.telegram.org/bot{BOT_TOKEN}/setMyCommands"
commands = [
    {"command": "start", "description": "Перезапустить бота"},
    {"command": "help", "description": "Помощь"},
    {"command": "post", "description": "Написать и разослать пост"},
    {"command": "addchannel", "description": "Добавить канал с языком"},
    {"command": "languages", "description": "Доступные языки для перевода"},
    {"command": "dellchannel", "description": "удалить канал"}
]

response = requests.post(url, json={"commands": commands})
print(response.json())


if __name__ == "__main__":
    print("Бот запущен")
    bot.infinity_polling(none_stop=True, skip_pending=True)
