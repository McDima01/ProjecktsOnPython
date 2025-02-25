import sys
import telebot
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

print("Это работает")
TOKEN = "7308504315:AAFIYerV5gfUQy5pZVk2MH1vzqvKFsEVy9o"
bot = telebot.TeleBot(TOKEN)
api_key = "cfac08670e6509c462cd35dd"
ADMIN_CHAT_ID = 5038901733


@bot.message_handler(commands=["start"])
def user_info(message):
    print(f"Пользователь {message.from_user.first_name} ID-{message.from_user.id} запустил(a) бота")
    bot.send_message(
        message.chat.id,
        f"Здравствуйте, {message.from_user.first_name}! \n"
        "Этот бот может:\n"
        "- Просматривать курсы валют через команду /rate\n"
        "- Конвертировать валюту через команду /convert",
        parse_mode="Markdown"
    )

@bot.message_handler(commands=["stop"])
def stopping_the_bot(message):
    if message.chat.id == ADMIN_CHAT_ID:
        bot.send_message(message.chat.id, f"{message.from_user.first_name}, вы точно хотите выключить бота?")

        # Создаем инлайн-клавиатуру с кнопками "Да" и "Нет"
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton("Да", callback_data="stop_confirmed"),
            InlineKeyboardButton("Нет", callback_data="stop_canceled")
        )
        bot.send_message(message.chat.id, "Нажмите 'Да', чтобы подтвердить, или 'Нет', чтобы отменить.",
                         reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, 'У вас недостаточно полномочий для этой команды!')

@bot.message_handler(commands=["rate"])
def ask_for_base_currency(message):
    """Запрос базовой валюты у пользователя для отображения курсов валют."""
    bot.send_message(
        message.chat.id,
        "Введите код базовой валюты (например, USD, EUR) или выберите из предложенных:",
        parse_mode="Markdown"
    )

    # Создаем инлайн-кнопки для популярных валют
    keyboard = InlineKeyboardMarkup()
    currencies = ["USD", "EUR", "RUB", "KZT", "JPY", "UAH", "CNY"]
    for currency in currencies:
        keyboard.add(InlineKeyboardButton(currency, callback_data=f"rate_{currency}"))
    bot.send_message(message.chat.id, "Выберите одну из валют:", reply_markup=keyboard)

@bot.message_handler(commands=["convert"])
def start_conversion(message):
    """Начало процесса конвертации валют."""
    bot.send_message(
        message.chat.id,
        "Введите запрос в формате: <сумма> <валюта> - <целевая валюта>\nПример: 10 USD - RUB",
        parse_mode="Markdown"
    )

@bot.message_handler(content_types=["text"])
def handle_text(message):
    """Обработка текстовых сообщений."""
    user_input = message.text.strip().upper()

    # Если пользователь вводит данные для конверсии
    if "-" in user_input:
        try:
            # Убираем дефис и делим строку
            parts = user_input.replace("-", "").split()
            if len(parts) == 3 and parts[0].isdigit():
                amount = int(parts[0])  # Сумма
                base_currency = parts[1]  # Исходная валюта
                target_currency = parts[2]  # Целевая валюта

                # Запрос к API
                url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{base_currency}/{target_currency}/{amount}"
                response = requests.get(url)

                if response.ok:
                    data = response.json()
                    if "conversion_result" in data:
                        result = data["conversion_result"]
                        print(f"Пользователь {message.from_user.first_name} конвертировал {amount} {base_currency} в {target_currency}")
                        bot.send_message(
                            message.chat.id,
                            f"{amount} {base_currency} на данный момент равно {result:.2f} {target_currency}.",
                            parse_mode="Markdown"
                        )
                    else:
                        bot.send_message(message.chat.id, "Ошибка: данные о конверсии не найдены.")
                else:
                    bot.send_message(message.chat.id, "Ошибка подключения к API. Проверьте валюты.")
            else:
                bot.send_message(
                    message.chat.id,
                    "Некорректный ввод. Формат: <сумма> <базовая_валюта> - <целевая_валюта>"
                )
        except Exception as e:
            bot.send_message(message.chat.id, f"Произошла ошибка: {e}")
    else:
        bot.send_message(
            message.chat.id,
            "Некорректный ввод. Используйте команду /rate или /convert."
        )

@bot.callback_query_handler(func=lambda call: call.data.startswith("rate_"))
def handle_rate_callback(call):
    """Обработка инлайн-кнопок для выбора базовой валюты."""
    base_currency = call.data.split("_")[1]

    # URL для получения курсов валют
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
    response = requests.get(url)

    if response.ok:
        data = response.json()
        rates = data.get("conversion_rates", {})
        if rates:
            print(f"Пользователь {call.from_user.first_name} запросил курсы валют для {base_currency}.")
            selected_currencies = ["USD", "EUR", "RUB", "KZT", "JPY", "UAH", "CNY"]

            rates_text = f"Текущие курсы валют к {base_currency}:\n"
            for currency in selected_currencies:
                rate = rates.get(currency, "Нет данных")
                rates_text += f"{currency}: {rate}\n"

            bot.send_message(call.message.chat.id, rates_text)
        else:
            bot.send_message(call.message.chat.id, "Не удалось получить курсы валют.")
    else:
        bot.send_message(call.message.chat.id, "Ошибка подключения к API. Проверьте код валюты.")

@bot.callback_query_handler(func=lambda call: call.data == "stop_confirmed")
def confirm_stop(call):
    if call.message.chat.id == ADMIN_CHAT_ID:
        bot.send_message(call.message.chat.id, "Бот останавливается. До свидания!")
        print(f"Бот остановлен пользователем {call.from_user.first_name}.")
        bot.stop_polling()  # Останавливаем процесс polling
        sys.exit(0)  # Завершаем программу
    else:
        bot.send_message(call.message.chat.id, 'У вас недостаточно полномочий для этой команды!')

@bot.callback_query_handler(func=lambda call: call.data == "stop_canceled")
def cancel_stop(call):
    if call.message.chat.id == ADMIN_CHAT_ID:
        bot.send_message(call.message.chat.id, "Операция отменена. Бот продолжает работать.")
        print(f"Пользователь {call.from_user.first_name} отменил остановку бота.")
    else:
        bot.send_message(call.message.chat.id, 'У вас недостаточно полномочий для этой команды!')



bot.infinity_polling()
