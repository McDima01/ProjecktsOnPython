import telebot
import re
import emoji  # pip install emoji
from telebot import TeleBot, types
from utilities import *

def register_handlers(bot: TeleBot):
    def checkTheAdminLeeBot(channel):
        try:
            msg = bot.send_message(channel, '.')
            bot.delete_message(channel, msg.message_id)
            return True
        except telebot.apihelper.ApiTelegramException as e:
            if "CHAT_WRITE_FORBIDDEN" in str(e):
                return False

    # обработка команды /start
    @bot.message_handler(commands=["start"])
    def welcome_skript(message):
        user_id = str(message.from_user.id)
        data = load_data()
        if user_id not in data:
            bot.send_message(message.chat.id,
                             f"Здравствуйте, {message.from_user.first_name}! С помощью этого бота можно делать рассылки которые будут переводится на разные языки и отправляться в каналы которые вы укажете!")
            bot.send_message(message.chat.id, 'Чтобы подробнее узнать про бота напишите /help')
            data[user_id] = {}
            save_data(data)
        else:
            bot.send_message(message.chat.id,
                             f"Здравствуйте, {message.from_user.first_name}! \nЧто хотите сделать?\n\n Вы можете: "
                             f"\n/post - Отправить пост.\n/addchannel - Добавить канал. \n/dellchannel - Удалить канал. \n/languages - Посмотреть доступные языки для перевода.")
        print(f'{message.from_user.first_name} ID - {user_id}  запустил(а) бота')

    # обработка команды /help
    @bot.message_handler(commands=["help"])
    def help_skript(message):
        bot.send_message(message.chat.id, 'Этот бот может переводить посты которые вы ему отправите и рассылать их по нужным каналам.\n'
                                          '\nПеред тем как добавлять канал в бота, сделайте бота администратором в вашем канале!\n'
                                          '\nЧтобы добавить канал напишите: "/addchannel <канал> <язык>" канал укажите в формате: @channel. \n'
                                          'Язык указывайте в формате: ru, en и т.д.\n'
                                          '\nЧтобы посмотреть список доступных языков для перевода напишите: /languages\n'
                                          '\nЧтобы удалить канал напишите "/dellchannel".\n'
                                          '\nЕсли вы уже добавили канал и язык, то напишите команду /post чтобы написать пост и отправить рассылку.')

    # Добавление канала
    @bot.message_handler(commands=["addchannel"])
    def add_channel(message):
        user_id = str(message.from_user.id)
        user_channel = message.text.split(" ")

        if len(user_channel) < 3:
            bot.send_message(message.chat.id, "Ошибка: недостаточно данных. Пример: /addChannel <канал> <язык>")
            return

        if not user_channel[1].startswith('@'):
            bot.send_message(message.chat.id, 'Канал обязательно должен начинаться со знака "@"!')
            return

        data = load_data()

        # Проверка на наличие данных для пользователя
        if user_id not in data:
            data[user_id] = {}

        # Проверка, если канал уже добавлен в data
        i = 1
        while f"channel_id{i}" in data[user_id]:
            # Если такой канал уже есть, выводим сообщение и выходим
            if data[user_id][f"channel_id{i}"] == user_channel[1]:
                bot.send_message(message.chat.id, f"Этот канал ({user_channel[1]}) уже был добавлен.")
                return
            i += 1


        # Словарь языков (сокращение -> полное название)
        LANGUAGES = {
            "af": "Африкаанс", "sq": "Албанский", "am": "Амхарский", "ar": "Арабский",
            "hy": "Армянский", "as": "Ассамский", "ay": "Аймара", "az": "Азербайджанский",
            "bm": "Бамбара", "eu": "Баскский", "be": "Белорусский", "bn": "Бенгальский",
            "bho": "Бходжпури", "bs": "Боснийский", "bg": "Болгарский", "ca": "Каталанский",
            "ceb": "Себуанский", "ny": "Чева", "zh-CN": "Китайский (упрощенный)",
            "zh-TW": "Китайский (традиционный)", "co": "Корсиканский", "hr": "Хорватский",
            "cs": "Чешский", "da": "Датский", "nl": "Голландский", "en": "Английский",
            "eo": "Эсперанто", "et": "Эстонский", "fi": "Финский", "fr": "Французский",
            "de": "Немецкий", "el": "Греческий", "hi": "Хинди", "hu": "Венгерский",
            "is": "Исландский", "id": "Индонезийский", "it": "Итальянский", "ja": "Японский",
            "ko": "Корейский", "la": "Латынь", "lv": "Латышский", "lt": "Литовский",
            "ms": "Малайский", "mt": "Мальтийский", "no": "Норвежский", "pl": "Польский",
            "pt": "Португальский", "ro": "Румынский", "ru": "Русский", "sr": "Сербский",
            "sk": "Словацкий", "sl": "Словенский", "es": "Испанский", "sv": "Шведский",
            "th": "Тайский", "tr": "Турецкий", "uk": "Украинский", "vi": "Вьетнамский",
            "cy": "Валлийский", "xh": "Коса", "yi": "Идиш", "yo": "Йоруба", "zu": "Зулусский"
        }

        # Получаем полное название языка
        language_name = LANGUAGES.get(user_channel[2].lower(), user_channel[2].upper())

        if checkTheAdminLeeBot(user_channel[1]):
            # Если не нашли повторяющегося канала, добавляем новый
            data[user_id][f"channel_id{i}"] = user_channel[1]
            data[user_id][f"lang{i}"] = user_channel[2].lower()
            save_data(data)

            # Отправляем сообщение с полным названием языка
            bot.send_message(message.chat.id,
                             f"Канал {user_channel[1]} с языком \"{language_name}\" был сохранен!")
        else:
            bot.send_message(user_id,
                             f"❌ Бот не может отправить сообщение в {user_channel[1]}, так как у него нет прав администратора!")

    # Функция показа какие каналы доступны для удаления
    @bot.message_handler(commands=["dellchannel"])
    def delete_channel(message):
            user_id = str(message.from_user.id)
            data = load_data()

            if user_id not in data:
                bot.send_message(message.chat.id, "У вас нет добавленных каналов.")
                return

            channels_list = []
            for i in range(1, 6):  # Ожидаем, что максимум 5 каналов у пользователя
                channel_id = data[user_id].get(f"channel_id{i}")
                lang = data[user_id].get(f"lang{i}")
                if channel_id:
                    # Вместо channel_id, можем выводить название канала или другие данные
                    button = types.KeyboardButton(text=f"Удалить {channel_id} ({lang})")
                    channels_list.append(button)

            if channels_list:
                keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                keyboard.add(*channels_list)
                bot.send_message(message.chat.id, "Выберите канал для удаления:", reply_markup=keyboard)
            else:
                bot.send_message(message.chat.id, "У вас нет добавленных каналов.")

    # Функция удаления канала
    @bot.message_handler(func=lambda message: message.text.startswith('Удалить'))
    def handle_remove_channel(message):
        user_id = str(message.from_user.id)
        data = load_data()

        if user_id not in data:
            bot.send_message(message.chat.id, "Ошибка: вы не добавляли каналы.")
            return

        # Извлекаем канал из текста кнопки
        channel_info = message.text.replace('Удалить ', '')
        for i in range(1, 6):
            channel_id = data[user_id].get(f"channel_id{i}")
            if channel_id == channel_info.split(' ')[0]:  # Пытаемся найти канал по ID
                # Удаляем канал
                del data[user_id][f"channel_id{i}"]
                del data[user_id][f"lang{i}"]
                save_data(data)
                bot.send_message(message.chat.id, f"Канал {channel_info} был удалён.")
                return

        bot.send_message(message.chat.id, f"Канал {channel_info} не найден.")


    @bot.message_handler(commands=["post"])
    def sendPost(message):
        bot.send_message(message.chat.id, 'Теперь напишите пост и отправьте мне.')
        bot.register_next_step_handler(message, transferAndSendAPost)

    def transferAndSendAPost(message):
        user_id = str(message.from_user.id)
        data = load_data()

        # Если пришло изображение, гифка или видео
        if message.photo or message.animation or message.video:
            media_type = None
            file_id = None
            text = message.caption if message.caption else ""  # Подпись (если есть)

            if message.photo:
                media_type = "photo"
                file_id = message.photo[-1].file_id  # Берем самое большое изображение
            elif message.animation:
                media_type = "animation"  # Гифка
                file_id = message.animation.file_id
            elif message.video:
                media_type = "video"
                file_id = message.video.file_id

            for i in range(1, 51):  # Максимум 50 каналов
                channel_key = f"channel_id{i}"
                lang_key = f"lang{i}"

                if channel_key in data[user_id]:  # Если канал есть
                    channel_id = data[user_id][channel_key]
                    lang = data[user_id].get(lang_key, "ru")  # Язык по умолчанию — русский

                    translated_text = translator(text, lang) if text else ""

                    # Если подпись меньше 1024 символов — отправляем в caption
                    if len(translated_text) <= 1024:
                        send_media(bot, channel_id, media_type, file_id, translated_text)
                    else:
                        send_media(bot, channel_id, media_type, file_id, "")  # Без подписи
                        bot.send_message(channel_id, translated_text)  # Текст отдельно

            bot.send_message(message.chat.id, "Медиа-файл успешно отправлен во все каналы!")
            welcome_skript(message)

        else:
            # Если только текст
            user_text = message.text

            if not user_text:
                bot.send_message(message.chat.id, "Ошибка: вы не прислали текст для перевода.")
                return

            for i in range(1, 51):  # Максимум 50 каналов
                channel_key = f"channel_id{i}"
                lang_key = f"lang{i}"

                if channel_key in data[user_id]:  # Если канал есть
                    channel_id = data[user_id][channel_key]
                    lang = data[user_id].get(lang_key, "ru")

                    try:
                        translated_text = translator(user_text, lang)
                        bot.send_message(channel_id, translated_text)
                    except Exception as e:
                        bot.send_message(message.chat.id, f"Ошибка при переводе: {str(e)}")
                        return

            bot.send_message(message.chat.id, "Пост отправлен во все каналы!")
            welcome_skript(message)

    def send_media(bot, chat_id, media_type, file_id, caption=""):
        if media_type == "photo":
            bot.send_photo(chat_id, file_id, caption=caption)
        elif media_type == "animation":
            bot.send_animation(chat_id, file_id, caption=caption)
        elif media_type == "video":
            bot.send_video(chat_id, file_id, caption=caption)

# мой код функции transferAndSendAPost
"""    def transferAndSendAPost(message):
        user_id = str(message.from_user.id)
        data = load_data()

        # Если пришло изображение
        if message.photo:
            photo = message.photo[-1].file_id  # Получаем самое большое изображение
            text = message.caption if message.caption else ""  # Получаем подпись, если есть

            try:
                # Проверка на длину подписи
                if text and len(text) > 1024:
                    raise ValueError("Подпись слишком длинная. Максимальная длина — 1024 символа.")

                # Переводим текст, если он есть
                if text:
                    for i in range(1, 51):  # Максимум 50 каналов
                        channel_key = f"channel_id{i}"
                        lang_key = f"lang{i}"

                        if channel_key in data[user_id]:  # Если такой канал есть
                            channel_id = data[user_id][channel_key]
                            lang = data[user_id].get(lang_key, "ru")  # Язык по умолчанию — русский

                            try:
                                translated_text = translator(text, lang)  # Переводим текст
                            except Exception as e:
                                bot.send_message(message.chat.id, f"Ошибка при переводе: {str(e)}")
                                return

                            # Отправляем картинку с подписью
                            bot.send_photo(channel_id, photo, caption=translated_text)

                    bot.send_message(message.chat.id, "Пост с изображением отправлен во все каналы!")
                else:
                    # Если нет подписи, просто отправляем картинку без текста
                    for i in range(1, 51):  # Максимум 50 каналов
                        channel_key = f"channel_id{i}"

                        if channel_key in data[user_id]:  # Если такой канал есть
                            channel_id = data[user_id][channel_key]

                            # Отправляем картинку без текста
                            bot.send_photo(channel_id, photo)

                    bot.send_message(message.chat.id, "Изображение отправлено во все каналы!")

                welcome_skript(message)

            except ValueError as e:
                bot.send_message(message.chat.id, str(e))  # Отправляем сообщение пользователю о слишком длинной подписи
            except Exception as e:
                bot.send_message(message.chat.id, f"Произошла ошибка: подпись сообщения слишком длинная! Максимальная длинна подписи - 1024 символа.")

        else:
            # Если только текст
            user_text = message.text

            if not user_text:  # Если текст пустой
                bot.send_message(message.chat.id, "Ошибка: вы не прислали текст для перевода.")
                return

            # Проход по всем каналам пользователя
            for i in range(1, 51):  # Максимум 50 каналов
                channel_key = f"channel_id{i}"
                lang_key = f"lang{i}"

                if channel_key in data[user_id]:  # Если такой канал есть
                    channel_id = data[user_id][channel_key]
                    lang = data[user_id].get(lang_key, "ru")  # Язык по умолчанию — английский
                    try:
                        translated_text = translator(user_text, lang)  # Переводим текст
                    except Exception as e:
                        bot.send_message(message.chat.id, f"Ошибка при переводе: {str(e)}")
                        return

                    # Отправляем текст
                    bot.send_message(channel_id, translated_text)  # Отправляем в канал

            bot.send_message(message.chat.id, "Пост отправлен во все каналы!")
            welcome_skript(message)

    @bot.message_handler(commands=['languages'])
    def send_language_list(message):
        languages = {
            'Английский': ('en', '🇬🇧'), 'Арабский': ('ar', '🇸🇦'), 'Армянский': ('hy', '🇦🇲'), 'Африкаанс': ('af', '🇿🇦'),
            'Белорусский': ('be', '🇧🇾'), 'Бенгальский': ('bn', '🇧🇩'), 'Болгарский': ('bg', '🇧🇬'),
            'Боснийский': ('bs', '🇧🇦'),
            'Венгерский': ('hu', '🇭🇺'), 'Вьетнамский': ('vi', '🇻🇳'), 'Голландский': ('nl', '🇳🇱'),
            'Греческий': ('el', '🇬🇷'),
            'Грузинский': ('ka', '🇬🇪'), 'Датский': ('da', '🇩🇰'), 'Иврит': ('iw', '🇮🇱'), 'Индонезийский': ('id', '🇮🇩'),
            'Ирландский': ('ga', '🇮🇪'), 'Испанский': ('es', '🇪🇸'), 'Исландский': ('is', '🇮🇸'),
            'Итальянский': ('it', '🇮🇹'),
            'Казахский': ('kk', '🇰🇿'), 'Каталанский': ('ca', '🇪🇸'), 'Китайский (традиционный)': ('zh-TW', '🇹🇼'),
            'Китайский (упрощенный)': ('zh-CN', '🇨🇳'), 'Корейский': ('ko', '🇰🇷'), 'Латынь': ('la', '🏛️'),
            'Латышский': ('lv', '🇱🇻'), 'Литовский': ('lt', '🇱🇹'), 'Македонский': ('mk', '🇲🇰'),
            'Малайский': ('ms', '🇲🇾'),
            'Мальтийский': ('mt', '🇲🇹'), 'Маори': ('mi', '🇳🇿'), 'Монгольский': ('mn', '🇲🇳'), 'Немецкий': ('de', '🇩🇪'),
            'Непальский': ('ne', '🇳🇵'), 'Норвежский': ('no', '🇳🇴'), 'Персидский': ('fa', '🇮🇷'),
            'Польский': ('pl', '🇵🇱'),
            'Португальский': ('pt', '🇵🇹'), 'Румынский': ('ro', '🇷🇴'), 'Русский': ('ru', '🇷🇺'), 'Сербский': ('sr', '🇷🇸'),
            'Словацкий': ('sk', '🇸🇰'), 'Словенский': ('sl', '🇸🇮'), 'Таджикский': ('tg', '🇹🇯'), 'Тайский': ('th', '🇹🇭'),
            'Турецкий': ('tr', '🇹🇷'), 'Украинский': ('uk', '🇺🇦'), 'Узбекский': ('uz', '🇺🇿'),
            'Филиппинский': ('tl', '🇵🇭'),
            'Финский': ('fi', '🇫🇮'), 'Французский': ('fr', '🇫🇷'), 'Хинди': ('hi', '🇮🇳'), 'Хорватский': ('hr', '🇭🇷'),
            'Чешский': ('cs', '🇨🇿'), 'Шведский': ('sv', '🇸🇪'), 'Эстонский': ('et', '🇪🇪'), 'Японский': ('ja', '🇯🇵'),
            'Зулусский': ('zu', '🇿🇦')
        }

        sorted_languages = sorted(languages.items())  # Сортировка по алфавиту

        message_text = "📜 *Доступные языки для перевода:*\n\n"
        for lang, (code, flag) in sorted_languages:
            message_text += f"{flag} *{lang}* — `{code}`\n"

        bot.send_message(message.chat.id, message_text, parse_mode="Markdown")
"""
# мой предыдущий код
"""from telebot import TeleBot, types
from utilities import *
sent_msg = None  # Храним последнее сообщение, чтобы его удалить

def register_handlers(bot: TeleBot):
    # обработка команды /start
    @bot.message_handler(commands=["start"])
    def welcome_skript(message):
        user_id = str(message.from_user.id)
        data = load_data()
        if user_id not in data:
            bot.send_message(message.chat.id,
                             f"Здравствуйте, {message.from_user.first_name}! С помощью этого бота можно делать рассылки которые будут переводится на разные языки и отправляться в каналы которые вы укажете!")
            bot.send_message(message.chat.id, 'Чтобы подробнее узнать про бота напишите /help')
            data[user_id] = {}
            save_data(data)
        else:
            bot.send_message(message.chat.id,
                             f"Здравствуйте, {message.from_user.first_name}! \nЧто хотите сделать?\n\n Вы можете: "
                             f"\n/post - Отправить пост.\n/addChannel - Добавить канал. \n/dellChannel - Удалить канал. ")
        print(f'{message.from_user.first_name} запустил(а) бота')

    # обработка команды /help
    @bot.message_handler(commands=["help"])
    def help_skript(message):
        bot.send_message(message.chat.id, 'Этот бот может переводить посты которые вы ему отправите и рассылать их по нужным каналам.\n'
                                          '\nПеред тем как добавлять канал в бота, добавьте бота в канал с правами администратора!\n'
                                          '\nЧтобы добавить канал напишите: "/addChannel <канал> <язык>" канал укажите в формате: @channel, язык указывайте в формате: ru, en и т.д.\n'
                                          'Чтобы удалить канал напишите "/dellChannel".\n'
                                          '\nЕсли вы уже добавили канал и язык, то напишите команду /post чтобы написать пост и отправить рассылку.')

    # Добавление канала
    @bot.message_handler(commands=["addChannel"])
    def add_channel(message):
        user_id = str(message.from_user.id)
        user_channel = message.text.split(" ")

        if len(user_channel) < 3:
            bot.send_message(message.chat.id, "Ошибка: недостаточно данных. Пример: /addChannel <канал> <язык>")
            return

        data = load_data()

        # Проверка на наличие данных для пользователя
        if user_id not in data:
            data[user_id] = {}

        # Проверка, если канал уже добавлен в data
        i = 1
        while f"channel_id{i}" in data[user_id]:
            # Если такой канал уже есть, выводим сообщение и выходим
            if data[user_id][f"channel_id{i}"] == user_channel[1]:
                bot.send_message(message.chat.id, f"Этот канал ({user_channel[1]}) уже был добавлен.")
                return
            i += 1

        # Если не нашли повторяющегося канала, добавляем новый
        data[user_id][f"channel_id{i}"] = user_channel[1]
        data[user_id][f"lang{i}"] = user_channel[2].lower()
        save_data(data)

        bot.send_message(message.chat.id,
                         f"Канал {user_channel[1]} с языком {user_channel[2].upper()} был сохранен!")

    # Функция показа какие каналы доступны для удаления
    @bot.message_handler(commands=["dellChannel"])
    def delete_channel(message):
            user_id = str(message.from_user.id)
            data = load_data()

            if user_id not in data:
                bot.send_message(message.chat.id, "У вас нет добавленных каналов.")
                return

            channels_list = []
            for i in range(1, 6):  # Ожидаем, что максимум 5 каналов у пользователя
                channel_id = data[user_id].get(f"channel_id{i}")
                lang = data[user_id].get(f"lang{i}")
                if channel_id:
                    # Вместо channel_id, можем выводить название канала или другие данные
                    button = types.KeyboardButton(text=f"Удалить {channel_id} ({lang})")
                    channels_list.append(button)

            if channels_list:
                keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                keyboard.add(*channels_list)
                bot.send_message(message.chat.id, "Выберите канал для удаления:", reply_markup=keyboard)
            else:
                bot.send_message(message.chat.id, "У вас нет добавленных каналов.")

    # Функция удаления канала
    @bot.message_handler(func=lambda message: message.text.startswith('Удалить'))
    def handle_remove_channel(message):
        user_id = str(message.from_user.id)
        data = load_data()

        if user_id not in data:
            bot.send_message(message.chat.id, "Ошибка: вы не добавляли каналы.")
            return

        # Извлекаем канал из текста кнопки
        channel_info = message.text.replace('Удалить ', '')
        for i in range(1, 6):
            channel_id = data[user_id].get(f"channel_id{i}")
            if channel_id == channel_info.split(' ')[0]:  # Пытаемся найти канал по ID
                # Удаляем канал
                del data[user_id][f"channel_id{i}"]
                del data[user_id][f"lang{i}"]
                save_data(data)
                bot.send_message(message.chat.id, f"Канал {channel_info} был удалён.")
                return

        bot.send_message(message.chat.id, f"Канал {channel_info} не найден.")

    @bot.message_handler(commands=["post"])
    def sendPost(message):
        bot.send_message(message.chat.id, 'Теперь напишите пост и отправьте мне.')
        bot.register_next_step_handler(message, transferAndSendAPost)

    # Функция обработки и отправки поста в каналы
    def transferAndSendAPost(message):
        user_text = message.text
        user_id = str(message.from_user.id)
        data = load_data()

        # Проход по всем каналам пользователя
        for i in range(1, 51):  # Максимум 50 каналов
            channel_key = f"channel_id{i}"
            lang_key = f"lang{i}"

            if channel_key in data[user_id]:  # Если такой канал есть
                channel_id = data[user_id][channel_key]
                lang = data[user_id].get(lang_key, "ru")  # Язык по умолчанию — английский
                translated_text = translator(user_text, lang)  # Переводим текст

                bot.send_message(channel_id, translated_text)  # Отправляем в канал

        bot.send_message(message.chat.id, "Пост отправлен во все каналы!")
        welcome_skript(message)

"""
