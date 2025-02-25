import time
import random
from time import sleep
import telebot
from events import events
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from json_tg import load_user_data, save_user_data, get_user_data, update_user_data, \
    reset_user_data  # Импортируем функции

print("Эта штука запустилась")
TOKEN = "6737672102:AAHbyU-EAshInf6oWQbakTREmO63BG5idvw"
bot = telebot.TeleBot(TOKEN)

# Функция для преобразования и выбора случайного события
def transform_and_choose_event(events):
    # Преобразуем каждый ивент
    for event in events:
        if "description" in event:
            description_parts = event["description"].split("\n", 1)
            event["description"] = description_parts[0]  # Первая часть как "description"
            if len(description_parts) > 1:
                event["question"] = description_parts[1]  # Вторая часть как "question"
    # Выбираем случайное событие
    selected_event = random.choice(events)
    return selected_event
# Преобразование и выбор события
selected_event = transform_and_choose_event(events)

def get_user_data(user_id):
    # Получаем данные пользователя из файла
    try:
        user_data = load_user_data()  # Загружаем данные
        if str(user_id) not in user_data:
            user_data[str(user_id)] = {
                "money": 50,  # Начальные данные
                "influence": 50,
                "level": 0,
                "wins": 0,
                "losses": 0,
                "selected_event": transform_and_choose_event(events)  # Событие, которое выбрал игрок
            }
            save_user_data(user_data)  # Сохраняем новые данные
    except KeyError:
        # Если данных нет, создаем новые
        user_data = {
            "money": 50,  # Начальные данные
            "influence": 50,
            "level": 0,
            "wins": 0,
            "losses": 0,
            "selected_event": transform_and_choose_event(events)  # Событие, которое выбрал игрок
        }
        save_user_data({str(user_id): user_data})  # Сохраняем новые данные
    return user_data[str(user_id)], user_data  # Возвращаем данные пользователя

# Отображаем изменения
def format_change(value):
    if value > 0:
        return f"увеличилось на {value}%"
    elif value < 0:
        return f"уменьшилось на {abs(value)}%"
    else:
        return "не изменилось"

# Функция для преобразования и выбора случайного события
def transform_and_choose_event(events):
    # Преобразуем каждый ивент
    for event in events:
        if "description" in event:
            description_parts = event["description"].split("\n", 1)
            event["description"] = description_parts[0]  # Первая часть как "description"
            if len(description_parts) > 1:
                event["question"] = description_parts[1]  # Вторая часть как "question"
    # Выбираем случайное событие
    selected_event = random.choice(events)
    return selected_event

@bot.message_handler(commands=["start"])
def wellcome_script(message):
    print(f"Пользователь {message.from_user.first_name} ID-{message.from_user.id} запустил(a) бота. \n")
    bot.send_message(message.chat.id,
                     "               Приветствую! \n \nЭто игра, в которой вам предстоит путешествовать и решать стоит ли делать то или иное действие. \n"
                     f"Если ваше состояние или влияние станут слишком низкими или высокими, вы проиграете. Так что держите баланс. Удачи! \n \nСейчас в игре {len(events)} cобытий."
                     f"\n \nЧтобы начать игру введите /start_game")

@bot.message_handler(commands=["start_game"])
def main_game(message):
    print(f"Пользователь {message.from_user.first_name} начал(а) новую игру")

    # Сбрасываем данные пользователя
    user_id = message.from_user.id
    reset_user_data(user_id)  # Добавляем сброс данных

    # Загружаем данные после сброса
    user_data, _ = get_user_data(user_id)

    # Извлекаем начальные значения
    money = user_data.get("money", 50)
    influence = user_data.get("influence", 50)
    level = user_data.get("level", 0)

    # Отправляем стартовое сообщение
    bot.send_message(message.chat.id, "Тогда начнём!")
    sleep(1.5)
    bot.send_message(message.chat.id, f"Ваше начальное состояние: Деньги — {money}%, Самооценка — {influence}%")

    # Отправляем описание первого события
    selected_event = transform_and_choose_event(events)
    bot.send_message(message.chat.id, selected_event['description'])

    # Создаём инлайн-клавиатуру для выбора
    keyboard = InlineKeyboardMarkup()
    currencies = ["да", "нет"]
    for currency in currencies:
        keyboard.add(InlineKeyboardButton(currency,  callback_data=f"выбор_{currency}"))

    # Отправляем вопрос
    bot.send_message(message.chat.id, selected_event["question"], reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith("выбор_"))
def handle_callback(call):
    global money, influence, level, selected_event

    user_id = call.from_user.id
    user_state, _ = get_user_data(user_id)  # Загружаем данные о пользователе

    # Инициализация данных, если они не существуют
    money = user_state.get("money", 50)
    influence = user_state.get("influence", 50)
    level = user_state.get("level", 0)
    selected_event = user_state.get("selected_event", selected_event)

    money_before = money
    influence_before = influence

    # Обработка выбора пользователя
    user_choice = call.data.split("_")[1]

    if user_choice == "да":
        bot.send_message(call.message.chat.id, selected_event["description_yes"])
        money += selected_event["money_change_yes"]
        influence += selected_event["influence_change_yes"]
        level += 1
    elif user_choice == "нет":
        bot.send_message(call.message.chat.id, selected_event["description_no"])
        money += selected_event["money_change_no"]
        influence += selected_event["influence_change_no"]
        level += 1

    money_change = money - money_before
    influence_change = influence - influence_before

    bot.send_message(call.message.chat.id,
                     f"Ваше состояние: Деньги — {money}% ({format_change(money_change)}), Самооценка — {influence}% ({format_change(influence_change)})")

    # Проверка достижения определённых уровней и поздравления
    if level in [5, 10, 15, 20, 25, 30, 35, 40, 45]:
        bot.send_message(call.message.chat.id, f"Поздравляю! Вы достигли уровня {level}!")
    elif level == 50:
        bot.send_message(call.message.chat.id, "Поздравляю! Вы достигли уровня 50! Вы победили!")
        bot.send_message(call.message.chat.id, "Если вы хотите начать заново напишите /start_game")
        update_user_data(call.from_user.id, 'win')

    # Обновляем данные пользователя
    update_user_data(user_id, {"money": money, "influence": influence, "level": level, "selected_event": selected_event})

    # Проверка завершения игры
    if money <= 0:
        bot.send_message(call.message.chat.id, "Игра окончена! Ваши деньги упали до 0%.")
        bot.send_message(call.message.chat.id, f"Вы достигли уровня {level}.")
        bot.send_message(call.message.chat.id, "Если вы хотите начать заново напишите /start_game")
        update_user_data(call.from_user.id, 'loss')  # Обновляем статистику при поражении
        return
    elif influence <= 0:
        bot.send_message(call.message.chat.id, "Игра окончена! Ваша самооценка упала до 0%.")
        bot.send_message(call.message.chat.id, f"Вы достигли уровня {level}.")
        bot.send_message(call.message.chat.id, "Если вы хотите начать заново напишите /start_game")
        update_user_data(call.from_user.id, 'loss')  # Обновляем статистику при поражении
        return
    elif money >= 100:
        bot.send_message(call.message.chat.id, "Игра окончена! Вы стали слишком богаты.")
        bot.send_message(call.message.chat.id, f"Вы достигли уровня {level}.")
        bot.send_message(call.message.chat.id, "Если вы хотите начать заново напишите /start_game")
        update_user_data(call.from_user.id, 'loss')  # Обновляем статистику при победе
        return
    elif influence >= 100:
        bot.send_message(call.message.chat.id, "Игра окончена! Ваша самооценка выросла до 100%.")
        bot.send_message(call.message.chat.id, f"Вы достигли уровня {level}.")
        bot.send_message(call.message.chat.id, "Если вы хотите начать заново напишите /start_game")
        update_user_data(call.from_user.id, 'loss')  # Обновляем статистику при победе
        return

    # Предупреждения при критическом уровне денег или влияния
    if money <= 20:
        bot.send_message(call.message.chat.id, "!ВНИМАНИЕ! Если ваши деньги достигнут 0%, вы проиграете.")
    elif influence <= 20:
        bot.send_message(call.message.chat.id, "!ВНИМАНИЕ! Если ваша самооценка достигнет 0%, вы проиграете.")
    elif money >= 80:
        bot.send_message(call.message.chat.id, "!ВНИМАНИЕ! Если ваши деньги достигнут 100%, вы проиграете.")
    elif influence >= 80:
        bot.send_message(call.message.chat.id, "!ВНИМАНИЕ! Если ваша самооценка достигнет 100%, вы проиграете.")

    time.sleep(1)  # Задержка перед отправкой ответа

    try:
        selected_event = transform_and_choose_event(events)
        user_state["selected_event"] = selected_event
        update_user_data(user_id, {"selected_event": selected_event})
        bot.send_message(call.message.chat.id, selected_event['description'])

        # Создаем клавиатуру для нового события
        keyboard = InlineKeyboardMarkup()
        currencies = ["да", "нет"]
        for currency in currencies:
            keyboard.add(InlineKeyboardButton(currency, callback_data=f"выбор_{currency}"))

        bot.send_message(call.message.chat.id, selected_event["question"], reply_markup=keyboard)
    except Exception as e:
        print(f"Ошибка при выборе нового события: {e}")
        bot.send_message(call.message.chat.id, "Произошла ошибка при выборе нового события. Попробуйте снова.")


bot.infinity_polling()
