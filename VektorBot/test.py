import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

# Токен вашего бота
bot = telebot.TeleBot("none")


bot.send_message(-1001622022510, "Ты ЛОХ!")

"""@bot.message_handler(commands=['start'])
def send_keyboard(message):
    markup = InlineKeyboardMarkup()

    # Кнопки с callback_data
    button1 = InlineKeyboardButton("Кнопка 1", callback_data="btn1")
    button2 = InlineKeyboardButton("Кнопка 2", callback_data="btn2")

    # Добавляем кнопки
    markup.add(button1, button2)

    bot.send_message(message.chat.id, "Выберите кнопку:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    # Получаем ID сообщения и ID чата
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    if call.data == "btn1":
        bot.answer_callback_query(call.id, "Вы нажали кнопку 1")
    elif call.data == "btn2":
        bot.answer_callback_query(call.id, "Вы нажали кнопку 2")

    # Убираем клавиатуру после нажатия кнопки
    bot.edit_message_reply_markup(chat_id, message_id, reply_markup=None)
"""
# Запуск бота
bot.polling()
