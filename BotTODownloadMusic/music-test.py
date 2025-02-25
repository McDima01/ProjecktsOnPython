import telebot
from config import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def asdas(message):
    bot.send_message(message.chat.id, "asdadasdasdasda")

bot.polling(none_stop=True)