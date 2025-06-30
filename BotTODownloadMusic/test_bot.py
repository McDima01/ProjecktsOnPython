import telebot

bot = telebot.TeleBot("none")

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply


from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

@bot.message_handler(commands=['start'])
def start(message):
    # Создаем клавиатуру с несколькими кнопками
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton("Кнопка 1")
    button2 = KeyboardButton("Кнопка 2")
    keyboard.add(button1, button2)

    bot.send_message(message.chat.id, "Выберите кнопку:", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == "Кнопка 1")
def button1_pressed(message):
    bot.send_message(message.chat.id, "Вы нажали на Кнопку 1!", reply_markup=ReplyKeyboardRemove())  # Убираем клавиатуру
    # Здесь можно отправить новое сообщение или выполнить другие действия

@bot.message_handler(func=lambda message: message.text == "Кнопка 2")
def button2_pressed(message):
    bot.send_message(message.chat.id, "Вы нажали на Кнопку 2!", reply_markup=ReplyKeyboardRemove())  # Убираем клавиатуру
    # Здесь тоже можно отправить новое сообщение или выполнить другие действия


def is_user_admin(user_id, channel_id):
    try:
        # Очищаем channel_id от пробелов и лишних символов
        channel_id = channel_id.strip()

        # Проверяем, начинается ли channel_id с @ (если нет, возможно, это chat_id)
        if not channel_id.startswith("@"):
            try:
                channel_id = int(channel_id)  # Пробуем привести к int (chat_id всегда число)
            except ValueError:
                bot.send_message(user_id, "Неверный формат channel_id! Используйте @username или числовой chat_id.")
                return False

        # Получаем список администраторов
        administrators = bot.get_chat_administrators(channel_id)

        # Проверяем, является ли пользователь администратором
        for admin in administrators:
            if admin.user.id == user_id:
                return True

        return False

    except Exception as e:
        print(f"Ошибка при проверке администратора: {e}")
        bot.send_message(user_id, f"Ошибка при проверке канала: {e}")
        return False

# Обработчик команды /getid в группах и ЛС
@bot.message_handler(commands=['getid'])
def get_chat_id(message):
    bot.send_message(message.chat.id, f"ID этого чата: `{message.chat.id}`", parse_mode="Markdown")

# Обработчик команды /getid в канале
@bot.channel_post_handler(func=lambda message: message.text and message.text.startswith("/getid"))
def get_channel_id(message):
    bot.send_message(message.chat.id, f"ID этого канала: `{message.chat.id}`", parse_mode="Markdown")

# Проверка команды /post
@bot.message_handler(commands=['post'])
def manual_post(message):
    user_id = message.chat.id
    bot.send_message(user_id, "Введите username или chat_id канала:")

    @bot.message_handler(func=lambda m: True)
    def get_channel(m):
        channel_id = m.text.strip()

        if is_user_admin(user_id, channel_id):
            bot.send_message(user_id, "Вы администратор канала! Начинаем публикацию.")
            # Тут логика публикации...
        else:
            bot.send_message(user_id, "Вы НЕ администратор этого канала!")


if __name__ == "__main__":
    print("Бот запущен")
    bot.polling()

"""import telebot
from telebot import types

bot = telebot.TeleBot("none")

# Храним данные о пользователях
user_data = {}

# Шаги
STEP_SELECT_PLAYLIST = 0
STEP_SELECT_CHANNEL = 1
STEP_SELECT_PERIODICITY = 2

# Словарь для сохранения состояния
user_steps = {}


# Запрос у пользователя плейлиста
def ask_playlist(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    playlists = ["Playlist 1", "Playlist 2", "Playlist 3"]  # Пример
    for playlist in playlists:
        markup.add(playlist)
    bot.send_message(message.chat.id, "Введите ID плейлиста в таком формате: 1007 \nЧтобы найти ID плейлиста, просто откройте его в браузере, кликните по ссылке и скопируйте цифры в конце.")


# Запрос у пользователя канала
def ask_channel(message):
    bot.send_message(message.chat.id, "Введите название канала в таком формате: @example")


# Запрос у пользователя периодичности
def ask_periodicity(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("Каждый час", "Каждый день", "Каждую неделю")  # Пример
    bot.send_message(message.chat.id, "Выберите периодичность публикации:", reply_markup=markup)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    user_data[message.chat.id] = {}
    user_steps[message.chat.id] = STEP_SELECT_PLAYLIST  # Начинаем с выбора плейлиста
    ask_playlist(message)


# Обработчик команды /post
@bot.message_handler(commands=['post'])
def manual_post(message):
    user_id = message.chat.id
    channel_id = message.text.strip()  # Например, пользователь присылает @channel_id

    # Проверяем, является ли пользователь администратором канала
    if not is_user_admin(user_id, channel_id):
        bot.send_message(user_id,
                         "Вы не являетесь администратором этого канала и не можете использовать бота для публикации.")
        return
    else:
        bot.send_message(user_id,
                         "Вы являетесь администратором этого канала, вы можете это сделать.")
    # Дальше идет обычная логика для публикации трека (например, выбор плейлиста и тд.)
    bot.send_message(user_id, "Выбор плейлиста и канал завершён. Бот будет публиковать музыку.")


# Проверка, является ли пользователь владельцем или администратором канала
def is_user_admin(user_id, channel_id):
    try:
        # Получаем список администраторов канала
        administrators = bot.get_chat_administrators(channel_id)

        # Проверяем, является ли пользователь администратором
        for admin in administrators:
            if admin.user.id == user_id:
                return True
        return False
    except Exception as e:
        print(f"Ошибка при проверке администратора: {e}")
        bot.send_message(user_id, f"Ошибка при проверке канала: {e}")
        return False


# Обработчик сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.chat.id

    # Если пользователь еще не начал процесс настройки
    if user_id not in user_steps:
        bot.send_message(user_id, "Для начала введите команду /start.")
        return

    # В зависимости от текущего шага, обрабатываем ввод
    if user_steps[user_id] == STEP_SELECT_PLAYLIST:
        user_data[user_id]["playlist"] = message.text
        user_steps[user_id] = STEP_SELECT_CHANNEL
        ask_channel(message)

    elif user_steps[user_id] == STEP_SELECT_CHANNEL:
        user_data[user_id]["channel"] = message.text
        user_steps[user_id] = STEP_SELECT_PERIODICITY
        ask_periodicity(message)

    elif user_steps[user_id] == STEP_SELECT_PERIODICITY:
        user_data[user_id]["periodicity"] = message.text
        bot.send_message(user_id,
                         f"Вы выбрали:\nПлейлист: {user_data[user_id]['playlist']}\nКанал: {user_data[user_id]['channel']}\nПериодичность: {user_data[user_id]['periodicity']}")
        bot.send_message(user_id, "Настройки завершены! Бот будет работать согласно выбранной периодичности.")
        user_steps[user_id] = None  # Завершаем настройку


# Запуск бота
if __name__ == "__main__":
    print("Бот запущен")
    bot.polling()
"""
