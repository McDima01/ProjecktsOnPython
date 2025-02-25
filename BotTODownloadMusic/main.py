import telebot
import yandex_music
import requests
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TPE1
import os
import random
import schedule
import time
from threading import Thread

# Токены
BOT_TOKEN = "7903459505:AAHgn0EqSDM0MGEg83_Q3md64JL5KbGHjTE"  # Токен Telegram-бота
CHANNEL_ID = "@skndaas"    # skndaas | UnLocal_Music_Dima Юзернейм канала
YANDEX_TOKEN = "y0_AgAAAABDhj-hAAG8XgAAAAD0l-71d-tAtkShSJmSC-TWb0MIuX7hovs"  # Токен Yandex Music

# Инициализация
bot = telebot.TeleBot(BOT_TOKEN)
client = yandex_music.Client(YANDEX_TOKEN).init()

# Сохранение ИД сообщения
sent_msg = None

# Папка для сохранения треков
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Функция скачивания трека
def get_track(track):
    track_name = f"{track.artists[0].name} - {track.title}.mp3"
    track_path = os.path.join(DOWNLOAD_DIR, track_name)

    cover_name = f"{track.artists[0].name} - {track.title}.jpg"
    cover_path = os.path.join(DOWNLOAD_DIR, cover_name)

    # Скачивание трека
    track.download(track_path)
    print(f"Трек '{track_name}' успешно скачан!")

    # Скачивание обложки
    cover_url = track.cover_uri.replace('%%', '1000x1000')
    response = requests.get(f"https://{cover_url}")
    with open(cover_path, 'wb') as f:
        f.write(response.content)
    print(f"Обложка для трека '{track_name}' загружена!")

    # Встраивание обложки в трек
    audio = MP3(track_path, ID3=ID3)
    try:
        audio.add_tags()
    except Exception:
        pass

    audio.tags.add(
        APIC(
            encoding=3,
            mime='image/jpeg',
            type=3,
            desc='Cover',
            data=open(cover_path, 'rb').read(),
        )
    )
    audio.tags.add(TIT2(encoding=3, text=track.title))
    audio.tags.add(TPE1(encoding=3, text=track.artists[0].name))
    audio.save()
    print(f"Обложка успешно встроена в трек '{track_name}'!")

    return track_path, cover_path

# Функция публикации случайного трека
def post_random_track():
    try:
        # Получаем треки, которые есть в "Мне нравится"
        tracks = client.users_likes_tracks()

        if not tracks:
            bot.send_message(5038901733, "Нет доступных треков!")
            print("Нет доступных треков!")
            return

        # Выбираем случайный трек
        track = random.choice(tracks)
        track = track.fetch_track()
        print(f"Выбран трек: {track.title}")
        bot.delete_message(5038901733, sent_msg.message_id)
        bot.send_message(5038901733, f"Выбран трек: {track.title}")

        # Скачиваем трек
        track_path, cover_path = get_track(track)
        if not os.path.exists(track_path):
            bot.send_message(5038901733, f"Файл трека '{track_path}' не найден!")
            print(f"Файл трека '{track_path}' не найден!")
            return

        # Публикуем трек
        with open(track_path, 'rb') as audio:
            with open(cover_path, 'rb') as cover:
                bot.send_audio(
                    CHANNEL_ID,
                    audio,
                    thumb=cover,  # Передаем файл обложки
                )
        print(f"\nТрек '{track.title}' опубликован в канал!")

        # Удаляем файл трека и обложки после публикации
        os.remove(track_path)
        os.remove(cover_path)
        print(f"Файлы '{track_path}' и '{cover_path}' удалены. \n \n ")

    except Exception as e:
        @bot.message_handler()
        def measdssg(message):
            bot.send_message(5038901733, f"Ошибка при публикации трека: {e}")
        print(f"Ошибка при публикации трека: {e}")

# Функция публикации через команду
@bot.message_handler(commands=['post'])
def manual_post(message):
    global sent_msg
    print("Пытаюсь скачать и запостить трек ")
    sent_msg = bot.send_message(message.chat.id, "Выбираю трек")
    try:
        post_random_track()
        bot.reply_to(message, f"Трек опубликован!")
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

# Запуск расписания для авто-публикации
def start_schedule():
    schedule.every(1).hours.do(post_random_track)


    bot.send_message(5038901733, f"Начинаю пост треков каждый час")

    while True:
        schedule.run_pending()
        time.sleep(1)

# Запускаем функцию в отдельном потоке
Thread(target=start_schedule).start()

# Запуск бота
print("Бот запущен")
bot.polling()
