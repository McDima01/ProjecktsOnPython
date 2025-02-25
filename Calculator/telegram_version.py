from asteval import Interpreter
import telebot
import re


print('Это работает')
token = "6868726533:AAHRP3n156rJJdbatBet2e-7y0HcAiWhz8w"
bot = telebot.TeleBot(token)


def calculate(user_input):
    move = ' '.join(user_input)  # Соединяем части в одну строку
    move = move.replace('÷', '/').replace('\\', '/').replace('×', '*')  # Заменяем '÷' и '\' на '/'
    aeval = Interpreter()  # Создаем интерпретатор
    try:
        result = aeval(move)  # Вычисляем результат
        return result
    except Exception as e:
        return f"Ошибка: {e}"


@bot.message_handler(commands=['start'])
def welcome_script(message):
    bot.send_message(message.chat.id,
                     f"Здравствуйте {message.from_user.first_name}.\nЭто бот-калькулятор\nДля того чтобы начать, просто введите выражение через пробел")
    print(f'Пользователь {message.from_user.first_name} запустил(а) бота')


@bot.message_handler(content_types=["text"])
def main_script(message):
    user_input = message.text.strip()

    # Проверка на наличие операторов в выражении
    if not re.search(r'[+\-*/]', user_input):
        bot.send_message(message.chat.id, "Пожалуйста, используйте хотя бы один оператор (+, -, *, /) в выражении.")
        return

    user_input = user_input.split(' ')
    result = calculate(user_input)
    expression = ' '.join(user_input)  # Отобразить оригинальное выражение
    bot.send_message(message.chat.id, f'{expression} = {result}')


bot.infinity_polling()