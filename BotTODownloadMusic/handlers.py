from telebot import TeleBot
import yandex_music
from utils import load_data, save_data
from yandex_music_utils import get_playlist_tracks, get_track, download_track
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import YANDEX_TOKEN
import random
import os
import threading
import schedule
import time
from telebot import types

sent_msg = None  # Храним последнее сообщение, чтобы его удалить
def run_scheduler():
    """Фоновая задача для запуска расписания"""
    while True:
        schedule.run_pending()
        time.sleep(1)  # Каждую секунду проверяем задачи
client = yandex_music.Client(YANDEX_TOKEN).init()
active_jobs = {} # Глобальный список активных задач (чтобы не запускать дублирующие потоки)

def register_handlers(bot: TeleBot):

    # Пост рандомного трека
    def post_random_track(user_id, chat_id=None):
        global sent_msg
        try:
            data = load_data()
            user_channel_id = data.get(str(user_id), {}).get("channel_id")

            if not user_channel_id:
                bot.send_message(chat_id, "Вы не указали ID канала! Введите его через /settings.")
                return

            playlist_url = data.get(str(user_id), {}).get("playlist_url")
            if not playlist_url:
                bot.send_message(chat_id, "Вы не указали ссылку на плейлист! Введите её через /settings.")
                return

            tracks = get_playlist_tracks(playlist_url)
            if not tracks:
                bot.send_message(chat_id, "Нет доступных треков в этом плейлисте!")
                return

            # Выбор случайного трека
            track = random.choice(tracks).fetch_track()
            track_path, cover_path = get_track(track)

            # ✅ Проверяем, есть ли сообщение, прежде чем удалить его
            if sent_msg:
                try:
                    bot.delete_message(chat_id, sent_msg.message_id)
                except Exception as e:
                    print(f"⚠️ Не удалось удалить сообщение (возможно, его нет): {e}")

            # Отправляем информацию о треке
            sent_msg = bot.send_message(chat_id, f"Выбран трек: {track.artists[0].name} - {track.title}")
            caption = "@downloader_yamusic_bot"


            # Отправляем аудиофайл в канал
            with open(track_path, 'rb') as audio, open(cover_path, 'rb') as cover:
                bot.send_audio(user_channel_id, audio, thumb=cover)

            os.remove(track_path)
            os.remove(cover_path)

        except Exception as e:
            print(f"Ошибка при публикации трека: {e}")
            bot.send_message(chat_id, f"Ошибка при публикации трека: {e}")

    # Обработка команды /start
    @bot.message_handler(commands=["start"])
    def welcome_skript(message, userid=None):
        data = load_data()
        user_id = str(message.from_user.id)
        username = message.from_user.username
        if user_id is None:
            user_id = userid
        print(f"{message.from_user.first_name} (@{username}) запустил(а) бота.")
        # Проверяем, если пользователь не существует в данных, добавляем его
        if user_id not in data:
            data[user_id] = {"user_name": f"@{username}","channel_id": None,"playlist_url": "https://music.yandex.ru/users/dimas.rav/playlists/1007", "post_interval": 3600,
                             "random_order": False, "last_posted": 0, 'prem': False, "end_prem": True, "admin": False, "setting_step": None}
            save_data(data)  # Сохраняем данные в файл


            bot.send_message(message.from_user.id,
                             f'Здравствуйте, {message.from_user.first_name}! \nЭтот бот может загрузить музыку в ваш канал. \nЧтобы настроить бота напишите /settings. '
                             f'\nЧтобы скачать любой трек напишите /download <ссылка на трек>.')
        else:
            bot.send_message(message.from_user.id, f"Здравствуйте, {message.from_user.first_name}! \nЧто вы хотите сделать? \nВы можете запостить музыку командой: \n/post. "
                                                   f"\nИли вы можете скачать трек командой: \n/download <ссылка на трек>.")

    # region Настройка
    # Обработка команды /settings
    @bot.message_handler(commands=['settings'])
    def settings_save(message):
        data = load_data()
        user_id = str(message.from_user.id)

        bot.send_message(message.from_user.id, "Начнем настройку! \nПеред тем как начать настройку обязательно добавьте бота в канал")
        bot.send_message(message.from_user.id, "Для начала напишите ID своего канала, в таком формате: -1002294633563."
                                          "\nЧтобы получить ID вашего канала: добавьте бота в ваш канал и напишите /getid в канал.")
        data[user_id]["setting_step"] = "get_channel_id"
        save_data(data)
        if data[user_id]["setting_step"] == "ended":
            bot.send_message(message.from_user.id, 'Вы уже настроили бота. Вы уверенны что хотите перенастроить бота?')
            bot.register_next_step_handler(message, continie)

    # если пользователь хочет настроить бота когда бот уже настроен
    def continie(message):
        user_response = message.text.lower()
        user_id = str(message.from_user.id)
        data = load_data()
        if user_response == "да":
            data[user_id]["setting_step"] = None
            save_data(data)
            bot.send_message(message.chat.id, 'Хорошо, чтобы перенастроить бота напишите: /settings')
        else:
            bot.send_message(message.chat.id, 'Хорошо, бот не будет перенастроен.')
            welcome_skript(message)

    # Получение ID канала пользователя
    @bot.message_handler(func=lambda message: load_data().get(str(message.chat.id), {}).get("setting_step") == "get_channel_id")
    def get_channel_id(message):
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text="Как узнать ссылку на плейлист?", callback_data="find_out_id")
        keyboard.add(button)
        user_id = str(message.from_user.id)
        data = load_data()

        try:
            user_channel = int(message.text)
            data[user_id]["channel_id"] = user_channel
            save_data(data)

            bot.send_message(message.chat.id,
                             f'Хорошо! сохранил {user_channel} как ID вашего канала.\n \nТеперь напишите ссылку на плейлист откуда вы хотите скачивать музыку. \n'
                             f'Из этого плейлиста или альбома я буду брать музыку для вашего канала!',
                             reply_markup=keyboard)
        except ValueError:
            bot.send_message(message.chat.id, "Пожалуйста, напишите ваш ID канала цифрами!")
            bot.register_next_step_handler(message, get_channel_id)


        data[user_id]["setting_step"] = "get_playlist_url"
        save_data(data)

    # Помощь как найти ID плейлиста\альбома
    @bot.callback_query_handler(func=lambda call: call.data == "find_out_id")
    def find_out_id_handler(call):
        bot.send_message(call.message.chat.id, "Чтобы найти ссылку на плейлист зайдите в приложение, "
                                               "откройте плейлист (главное чтобы он был открытый) и нажмите кнопку \"поделится\" и скопируйте ссылку на плейлист.")

    # Получение ID плейлиста пользователя
    @bot.message_handler(func=lambda message: load_data().get(str(message.chat.id), {}).get("setting_step") == "get_playlist_url")
    def get_playlist_id(message):
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text="Да, пусть буду вперемешку!", callback_data="yes")
        button1 = types.InlineKeyboardButton(text='Нет, пусть идут по порядку.', callback_data="no")
        keyboard.add(button, button1)
        user_playlist = message.text
        user_id = str(message.from_user.id)
        data = load_data()

        data[user_id]["playlist_url"] = user_playlist
        save_data(data)

        bot.send_message(message.chat.id, f'Отлично! Сохранил {user_playlist} как URL плейлиста из которого буду постить музыку!')
        bot.send_message(message.chat.id, f'Теперь скажите, можно будет перемешать треки в плейлисте или они будут постится по порядку?', reply_markup=keyboard)

        data[user_id]["setting_step"] = "tracks_in_mixing_or_not"
        save_data(data)

    # Если пользователь ответил "Да" на вопрос будет ли плейлист вперемешку
    @bot.callback_query_handler(func=lambda call: call.data == "yes")
    def find_out_id_handler(call):
        # Создаем клавиатуру с несколькими кнопками
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        button = KeyboardButton("Каждый час")
        button1 = KeyboardButton("Каждые 12 часов")
        button2 = KeyboardButton("каждый день")
        keyboard.add(button, button1, button2)
        user_id = str(call.from_user.id)
        data = load_data()

        data[user_id]['random_order'] = True
        save_data(data)

        bot.send_message(call.message.chat.id, 'Хорошо! Теперь треки из плейлиста будут поститься вперемешку!')
        bot.send_message(call.message.chat.id, 'Теперь выберете или напишите свой вариант с какой периодичностью будут поститься треки, '
                                               'если будете писать свой вариант то пишите в секундах и только число.', reply_markup=keyboard)


        data[user_id]['setting_step'] = 'the_interval_of_the_post_of_tracks'
        save_data(data)

    # Если пользователь ответил "Нет" на вопрос будет ли плейлист вперемешку
    @bot.callback_query_handler(func=lambda call: call.data == "no")
    def no_handler(call):
        # Создаем клавиатуру с несколькими кнопками
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        button = KeyboardButton("Каждый час")
        button1 = KeyboardButton("Каждые 12 часов")
        button2 = KeyboardButton("Каждый день")
        keyboard.add(button, button1, button2)
        user_id = str(call.from_user.id)
        data = load_data()

        bot.send_message(call.message.chat.id, 'Окей, плейлист будет поститься по порядку!')
        bot.send_message(call.message.chat.id, 'Теперь выберете или напишите свой вариант с какой периодичностью будут поститься треки, '
                                               'если будете писать свой вариант то пишите в секундах и только число.', reply_markup=keyboard)

        data[user_id]['setting_step'] = 'the_interval_of_the_post_of_tracks'
        save_data(data)

    # Спрашиваю у пользователя с каким интервалом постить треки
    @bot.message_handler(func=lambda message: load_data().get(str(message.chat.id), {}).get("setting_step") == "the_interval_of_the_post_of_tracks")
    def select_post_interval(message):
        user_post_interval = message.text
        user_id = str(message.from_user.id)
        data = load_data()

        # Проверка, существует ли user_id в данных
        if user_id not in data:
            bot.send_message(message.chat.id, "Пользователь не найден. Повторите настройку.")
            return

        # Установка интервала по выбранным вариантам
        if user_post_interval == 'Каждый час':
            bot.send_message(message.chat.id, 'Хорошо, буду постить музыку каждый час', reply_markup=ReplyKeyboardRemove())
            data[user_id]["post_interval"] = 3600
        elif user_post_interval == 'Каждые 12 часов':
            bot.send_message(message.chat.id, 'Хорошо, буду постить музыку каждые 12 часов ', reply_markup=ReplyKeyboardRemove())
            data[user_id]["post_interval"] = 43200
        elif user_post_interval == 'Каждый день':
            bot.send_message(message.chat.id, 'Хорошо, буду постить музыку каждый день ', reply_markup=ReplyKeyboardRemove())
            data[user_id]["post_interval"] = 86400
        else:
            try:
                # Попытка преобразования текста в число (интервал в секундах)
                user_post_interval = int(message.text)
                if user_post_interval <= 1:
                    raise ValueError("Интервал должен быть положительным числом.")

                if user_post_interval < 1800:
                    bot.send_message(user_id, "Нельзя постить треки чаще чем 30мин.")
                    return

                # Перевод в часы и отправка сообщения
                for_user_post_interval = round(user_post_interval / 3600, 1)
                bot.send_message(message.chat.id,
                                 f'Хорошо, буду постить музыку каждый {for_user_post_interval} час(ов)')
                data[user_id]["post_interval"] = user_post_interval
            except ValueError:
                bot.send_message(message.chat.id, "Ошибка: введите корректное число для интервала (в секундах).")
                return

        # Сохраняем данные
        save_data(data)
        data[user_id]["setting_step"] = "ended"
        save_data(data)
        if data[user_id]["setting_step"] == "ended":
            end_of_the_settings(message)

    # Показываю пользователю какие настройки он применил
    def end_of_the_settings(message):
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text="Да, всё верно!", callback_data="yess")
        button1 = types.InlineKeyboardButton(text='Нет, что-то не так.', callback_data="noo")
        keyboard.add(button, button1)
        data = load_data()
        user_id = str(message.from_user.id)
        if data[user_id]["random_order"]:
            order = "Да"
        else:
            order = "Нет"
        bot.send_message(message.chat.id, f'ID канала — {data[user_id]["channel_id"]} \nURL плейлиста — {data[user_id]["playlist_url"]} '
                                          f'\nИнтервал поста — {data[user_id]["post_interval"]} секунд \nБудет ли плейлист вперемешку — {order}')
        bot.send_message(message.chat.id, 'Всё верно?', reply_markup=keyboard)

    # Если пользователь ввёл всё правильно
    @bot.callback_query_handler(func=lambda call: call.data == "yess")
    def find_out_id_handler(call):
        user_id = str(call.from_user.id)
        data = load_data()

        data[user_id]['random_order'] = True
        save_data(data)

        bot.send_message(call.message.chat.id, 'Отлично! Возвращаю вас на главную!')
        welcome_skript(call, user_id)

    # Если пользователь ввёл что-то не правильно
    @bot.callback_query_handler(func=lambda call: call.data == "noo")
    def no_handler(call):
        user_id = str(call.from_user.id)
        data = load_data()

        bot.send_message(call.message.chat.id, 'Окей, возвращаю вас на начало настройки')


        data[user_id]['setting_step'] = None
        save_data(data)
        settings_save(call)
    # endregion

    #Обработка команды /download
    @bot.message_handler(commands=["download"])
    def download_track_on_url(message):
        user_id = message.from_user.id
        try:
            user_url = message.text.split(" ")
            track_path, cover_path = download_track(user_url[1])

            # Отправляем аудиофайл пользователю
            with open(track_path, 'rb') as audio, open(cover_path, 'rb') as cover:
                bot.send_audio(user_id, audio, thumb=cover)

            os.remove(track_path)
            os.remove(cover_path)
        except IndexError:
            bot.send_message(user_id, "Чтобы скачать трек напишите /download <ссылка>")

        welcome_skript(message, user_id)

    # Обработка команды /post
    @bot.message_handler(commands=["post"])
    def manual_post(message):
        global sent_msg
        user_id = str(message.from_user.id)  # Берем ID пользователя
        sent_msg = bot.send_message(message.chat.id, "Выбираю трек...")

        try:
            post_random_track(user_id, user_id)  # Передаем user_id
            bot.reply_to(message, "Трек опубликован!")
        except Exception as e:
            print(f"Ошибка: {e}")
            bot.reply_to(message, f"Ошибка: {e}")

    # Обработчик команды /getid в группах и ЛС
    @bot.message_handler(commands=["getid"])
    def get_chat_id(message):
        bot.send_message(message.chat.id, f"ID этого чата: `{message.chat.id}`", parse_mode="Markdown")

    # Обработчик команды /getid в канале
    @bot.channel_post_handler(func=lambda message: message.text and message.text.startswith("/getid"))
    def get_user_channel_id(message):
        bot.send_message(message.chat.id, f"ID этого канала: `{message.chat.id}`", parse_mode="Markdown")

    # Функция автопоста треков для пользователя
    def start_scheduled_posts(user_id):
        """Запускает автопостинг треков по интервалу пользователя"""
        data = load_data()

        if str(user_id) not in data or "post_interval" not in data[str(user_id)]:
            return

        interval = data[str(user_id)]["post_interval"]
        chat_id = data[str(user_id)].get("channel_id")
        user_name = data[str(user_id)]["user_name"]

        if not chat_id:
            return

        # Проверяем, нет ли уже задачи
        if user_id in active_jobs:
            return

        def post_track():
            print(f"🎵 Постинг трека для {user_name} ({user_id}) в {chat_id}...")
            post_random_track(user_id, user_id)

        # Добавляем задачу в общее расписание
        schedule.every(interval).seconds.do(post_track)

        active_jobs[user_id] = True

    # Функция остановки автопоста
    def stop_scheduled_posts(user_id):
        """Останавливает автопостинг для пользователя"""
        if user_id in active_jobs:
            del active_jobs[user_id]

    # Обработка команды /start_auto
    @bot.message_handler(commands=["start_auto"])
    def enable_autopost(message):
        data = load_data()
        user_id = str(message.from_user.id)
        user_post_interval = data[user_id]["post_interval"]
        interval = round(user_post_interval / 3600, 1)
        start_scheduled_posts(user_id)
        bot.send_message(message.chat.id, f"✅ Автопостинг запущен! Интервал: {interval} час(а).")
        post_random_track(user_id, user_id)

    # Обработка команды /stop_auto
    @bot.message_handler(commands=["stop_auto"])
    def disable_autopost(message):
        user_id = str(message.from_user.id)
        stop_scheduled_posts(user_id)
        bot.send_message(message.chat.id, "🛑 Автопостинг остановлен!")

"""    @bot.message_handler(commands=["premium"])
    def about_prem(message):
        user_id = str(message.from_user.id)
        data = load_data()

        if data[user_id]["prem"]:
            bot.send_message(message.chat.id, "У вас уже есть премиум! 😎 \n")

        else:
            bot.send_message(message.chat.id,
                             "Премиум делает так чтобы при отправке трека в канал не писался \"@downloader_yamusic_bot\", музыка будет отправляться без подписи! 🤯")
            if data[user_id]['end_prem']:
                keyboard = InlineKeyboardMarkup()

                button1 = InlineKeyboardButton("Купить премиум", callback_data="buy_premium")
                button2 = InlineKeyboardButton("Да", callback_data="yes_free")
                button3 = InlineKeyboardButton("Нет", callback_data="no_free")

                keyboard.add(button1)
                keyboard.add(button2, button3)  # Вторая строка с двумя кнопками
                bot.send_message(message.chat.id,
                                 "У меня есть для вас подарок, премиум на 14 дней! 😍 \nХотите ли вы его получить?",
                                 reply_markup=keyboard)



"""

# Запускаем в отдельном потоке
scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()
