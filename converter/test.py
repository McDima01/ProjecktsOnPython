import telebot
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "7308504315:AAFIYerV5gfUQy5pZVk2MH1vzqvKFsEVy9o"
bot = telebot.TeleBot(TOKEN)
api_key = "cfac08670e6509c462cd35dd"


@bot.message_handler(commands=["start"])
def user_info(message):
    print(f"Пользователь {message.from_user.first_name} ID-{message.from_user.id} запустил(a) бота")
    bot.send_message(
        message.chat.id,
        f"Здравствуйте, {message.from_user.first_name}! \n"
        "Этот бот может конвертировать валюты и следить за их курсом.\n"
        "Используйте команду /rate для просмотра курсов валют.\n"
        "Используйте команду /convert для конвертации валюты.",
        parse_mode="Markdown"
    )

@bot.message_handler(commands=["rate"])
def ask_for_base_currency(message):
    """Запрос базовой валюты у пользователя для отображения курсов валют."""
    bot.send_message(
        message.chat.id,
        "Введите валюту, от которой будут строиться курсы валют.\n"
        "Обязательно вводите тремя английскими буквами (например, USD, EUR):",
        parse_mode="Markdown"
    )

@bot.message_handler(commands=["convert"])
def start_conversion(message):
    """Начало процесса конвертации валют."""
    bot.send_message(
        message.chat.id,
        "Введите число валюты и валюту, в которую вы хотите конвертировать её. \n"
        "Пример: 10 eur - rub",
        parse_mode="Markdown"
    )

@bot.message_handler(content_types=["text"])
def handle_text(message):
    """Обработка текстовых сообщений для курсов валют и конверсии."""
    try:
        user_input = message.text.strip().upper()

        # Если пользователь вводит базовую валюту для команды /rate
        if len(user_input) == 3 and user_input.isalpha():
            base_currency = user_input

            # URL для получения курсов валют
            url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
            response = requests.get(url)

            if response.ok:
                data = response.json()
                rates = data.get("conversion_rates", {})
                if rates:
                    print(f"Пользователь {message.from_user.first_name} запросил курсы валют для {base_currency}.")
                    selected_currencies = ["USD", "EUR", "RUB", "KZT", "JPY", "UAH", "CNY"]

                    rates_text = f"Текущие курсы валют к {base_currency}:\n"
                    for currency in selected_currencies:
                        rate = rates.get(currency, "Нет данных")
                        rates_text += f"{currency}: {rate}\n"

                    bot.send_message(message.chat.id, rates_text)
                else:
                    bot.send_message(message.chat.id, "Не удалось получить курсы валют.")
            else:
                bot.send_message(message.chat.id, "Ошибка подключения к API. Проверьте код валюты.")

        # Если пользователь вводит данные для конверсии
        elif "-" in user_input:
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
        else:
            bot.send_message(
                message.chat.id,
                "Некорректный ввод. Используйте команду /rate или /convert."
            )
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}")

bot.infinity_polling()
