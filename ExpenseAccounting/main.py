"""
7. Приложение для учета расходов
   напишите программу, где пользователь может вести учет своих доходов и расходов, а также получать сводки.
"""
import telebot

print("Бот запустился")
TOKEN = "8166108581:AAEdhfYM0gnYurL2P-ervNsonbCSxvmkyK8"
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def welcome_skript(message):
    print(f'Пользователь {message.from_user.first_name} запустил(а) бота')



bot.infinity_polling()