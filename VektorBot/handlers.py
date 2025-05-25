from telebot import TeleBot, types
from config import *
from telebot.types import InputMediaPhoto, ReplyKeyboardMarkup
from telebot.types import KeyboardButton, ReplyKeyboardRemove
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import re

"""
    @bot.message_handler(commands=[''])
    def example(message):
        user_id = message.from_user.id
        if check_user_subscription(bot, user_id):
            # код странички 
        else:
            send_subscription_request(bot, user_id)
"""

def escape_markdown_v2(text):
    special_chars = r"\._[]()~`>#+-=|{}!<>"
    return re.sub(f"([{re.escape(special_chars)}])", r'\\\1', text)

def check_user_subscription(bot, user_id):
    status = bot.get_chat_member(CHANNEL_ID, user_id).status
    return status in ["member", "administrator", "creator"]

def send_subscription_request(bot, user_id):
    markup = types.InlineKeyboardMarkup()
    btn_subscribe = types.InlineKeyboardButton("\ud83d\udcE2 Подписаться", url=f"https://t.me/vectorbuilding    ")
    btn_check = types.InlineKeyboardButton("\ud83d\udd04 Проверить подписку", callback_data="check_sub")
    markup.add(btn_subscribe)
    markup.add(btn_check)
    bot.send_message(user_id, "\u274c Вы не подписаны на канал! Подпишитесь и нажмите \u00abПроверить подписку\u00bb.",
                     reply_markup=markup)

def register_handlers(bot: TeleBot):
    @bot.message_handler(commands=['start'])
    def start(message):
        user_id = message.from_user.id
        print(f"{message.from_user.first_name} ({user_id}) запустил(а) бота!")
        if check_user_subscription(bot, user_id):
                    bot.send_message(user_id, f"""👋 Здравствуйте, {message.from_user.first_name}!

🏗 Этот бот поможет вам узнать больше о строительных лесах с электрическим подъёмником ⚡️

❓ Чтобы получить дополнительную информацию о нас, отправьте команду: /aboutus 💡

❗ Можете попасть в меню по команде /menu ✅""")
        else:
            send_subscription_request(bot, user_id)

    @bot.message_handler(commands=['menu'])
    def main_menu(message):
        user_id = message.from_user.id
        if check_user_subscription(bot, user_id):
            bot.send_message(user_id, "Добро пожаловать в меню!\n \nВы можете:\n/contact - Связаться с нами,\n/feedback - Оставить отзыв, \n/info - Узнать подробнее о продукции,\n"
                                      "/rent - Узнать условия аренды, \n/help - Помощь.\n \n")
        else:
            send_subscription_request(bot, user_id)

    @bot.message_handler(commands=['rent'])
    def example(message):
        user_id = message.from_user.id
        markup = types.InlineKeyboardMarkup(row_width=2)

        button1 = types.InlineKeyboardButton("📋 Условия аренды", callback_data="leaseConditions")
        button2 = types.InlineKeyboardButton("📅 Сроки аренды", callback_data="datesForRent")
        button3 = types.InlineKeyboardButton("🚚 Доставка", callback_data="delivery")
        button4 = types.InlineKeyboardButton("💰 Стоимость", callback_data="value")
        button5 = types.InlineKeyboardButton("📞 Связаться с менеджером", callback_data="relateWithUs")

        markup.add(button1, button2)
        markup.add(button3, button4)
        markup.add(button5)
        if check_user_subscription(bot, user_id):
            bot.send_message(user_id, """🔧 К сожаленью на данный момент аренда строительных лесов с электроподъёмником не доступна.""")
        else:
            send_subscription_request(bot, user_id)

    # All Inline Keyboard handler
    @bot.callback_query_handler(func=lambda call: True)
    def handle_callback(call):
        user_id = call.from_user.id
        # region RENT
        if call.data == "leaseConditions":
            bot.send_message(user_id, "Hi")
        elif call.data == "datesForRent":
            bot.send_message(user_id, "Hi")
        elif call.data == "delivery":
            bot.send_message(user_id, "Hi")
        elif call.data == "value":
            bot.send_message(user_id, "Hi")
        elif call.data == "relateWithUs":
            bot.send_message(user_id, "Hi")
        # endregion
        # region FeedBack
        elif call.data == "leaveFeedback":
            sent = bot.send_message(user_id,r"""💬 Пожалуйста, напишите ваш отзыв о нашей продукции\. После проверки мы его выложим в [наш канал](t.me/vektor_feedback) с отзывами\.

Пожалуйста, если вы хотите остаться анонимными, напишите об этом в начале отзыва\!""",parse_mode="MarkdownV2")
            bot.register_next_step_handler(sent, leave_feedback)  # <-- ждём текстовый ответ и передаём его в leave_feedback
        elif call.data == 'seeFeedback':
            markup = types.InlineKeyboardMarkup(row_width=2)
            button1 = types.InlineKeyboardButton("✅ Отправить отзыв в канал", callback_data="sendReview")
            button2 = types.InlineKeyboardButton("💬 Изменить и отправить", callback_data="changeReview")
            button3 = types.InlineKeyboardButton("❌ Не опубликовывать", callback_data="NotPostAReview")
            markup.add(button1, button2)
            markup.add(button3)
            bot.send_message(user_id, f"Вот отзыв который отправил \"{first_namee}\" (@{usernamee}):")
            bot.send_message(user_id, user_feedbackk, reply_markup=markup)
        elif call.data == 'sendReview':
            chat_id = call.message.chat.id
            message_id = call.message.message_id
            user_feedback = f"{first_namee}: \n\n {user_feedbackk}"
            bot.send_message(REVIEW_CHANNEL_ID, user_feedback)
            bot.send_message(user_id, "Отзыв успешно отправлен в канал!")
            bot.edit_message_reply_markup(chat_id, message_id, reply_markup=None)
        elif call.data == 'changeReview':
            chat_id = call.message.chat.id
            message_id = call.message.message_id
            sent = bot.send_message(user_id, f"Вот текст отзыва, нажмите чтобы скопировать: \n `{user_feedbackk}`",
                                    parse_mode="MarkdownV2")
            bot.register_next_step_handler(sent, change_review)
            bot.edit_message_reply_markup(chat_id, message_id, reply_markup=None)
        elif call.data == "NotPostAReview":
            chat_id = call.message.chat.id
            message_id = call.message.message_id
            bot.send_message(user_id, "Хорошо, отзыв не будет опубликован в канал!")
            bot.edit_message_reply_markup(chat_id, message_id, reply_markup=None)
        elif call.data == 'yesFeedback':
            chat_id = call.message.chat.id
            message_id = call.message.message_id
            bot.send_message(REVIEW_CHANNEL_ID, admin_change_review)
            bot.send_message(user_id, "Изменённый отзыв успешно отправлен в канал!")
            bot.edit_message_reply_markup(chat_id, message_id, reply_markup=None)
        elif call.data == 'noFeedback':
            chat_id = call.message.chat.id
            message_id = call.message.message_id
            bot.send_message(user_id, "Хорошо, вы можете ещё раз изменить отзыв пользователя!")
            sent = bot.send_message(user_id, f"Вот текст отзыва, нажмите чтобы скопировать: \n `{user_feedbackk}`",
                                    parse_mode="MarkdownV2")
            bot.edit_message_reply_markup(chat_id, message_id, reply_markup=None)
            bot.register_next_step_handler(sent, change_review)
        # endregion
        if call.data == "check_sub":
            if check_user_subscription(bot, user_id):
                bot.edit_message_text("✅ Вы подписаны на канал! \nПожалуйста, ещё раз напишите /start",
                                      call.message.chat.id, call.message.message_id)
            else:
                bot.answer_callback_query(call.id, "❌ Вы ещё не подписаны!")
            return  # не даём идти дальше по остальным условиям

    def change_review(message):
        user_id = message.from_user.id
        global admin_change_review
        admin_change_review = message.text

        markup = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton("ДА", callback_data="yesFeedback")
        button2 = types.InlineKeyboardButton("НЕТ", callback_data="noFeedback")
        markup.add(button1, button2)

        bot.send_message(user_id, "Вы уверены что хотите отправить этот отзыв?", reply_markup=markup)

    def leave_feedback(message):
        global user_feedbackk, usernamee, first_namee
        user_id = message.from_user.id
        first_namee = message.from_user.first_name
        usernamee = message.from_user.username
        user_feedbackk = message.text

        markup = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton("Посмотреть отзыв", callback_data="seeFeedback")
        markup.add(button1)

        for admin in ADMINS:
            bot.send_message(admin, "У вас новый человек, который оставил отзыв, проверьте его и он опубликуется в канал!", reply_markup=markup)
        bot.send_message(user_id,
                         r"С радостью сообщаем вам, что ваш отзыв отправлен на проверку нашему менеджеру и в скоре он возможно появится в [нашем канале с отзывами](t.me/vektor_feedback)\!",
                         parse_mode="MarkdownV2")

    @bot.message_handler(commands=['aboutus'])
    def help_menu(message):
        user_id = message.from_user.id
        if check_user_subscription(bot, user_id):
            bot.send_message(user_id,
                             f"""🔹 Мы — первая в России компания с собственным производством, выпускающая строительные леса с электрическим подъёмником ⚡🏗

🔹 На данный момент у нас есть три основные модели:

🟢 ЭП20003 — высота подъёма 2 метра

🔵 ЭП40003 — высота подъёма 4 метра

🟠 ЭП60003 — высота подъёма 6 метров

📌 Узнать подробнее о моделях можно, отправив команду: /info 💬""")
        else:
            send_subscription_request(bot, user_id)

    @bot.message_handler(commands=['feedback'])
    def example(message):
        user_id = message.from_user.id
        markup = types.InlineKeyboardMarkup(row_width=2)

        button1 = types.InlineKeyboardButton("💭 Оставить отзыв", callback_data="leaveFeedback")
        button2 = types.InlineKeyboardButton("👁‍🗨 Посмотреть отзывы", url="t.me/vektor_feedback")

        markup.add(button1, button2)
        if check_user_subscription(bot, user_id):
            bot.send_message(user_id, "Выберите что вы хотите сделать:", reply_markup=markup)
        else:
            send_subscription_request(bot, user_id)

    @bot.message_handler(commands=['info'])
    def info_script(message):
        user_id = message.from_user.id
        if check_user_subscription(bot, user_id):
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            button = KeyboardButton("🟢 ЭП20003 — 2 метра")
            button1 = KeyboardButton("🔵 ЭП40003 — 4 метра")
            button2 = KeyboardButton("🟠 ЭП60003 — 6 метров")
            keyboard.add(button, button1, button2)
            bot.send_message(user_id, "📌 Выберите модель, о которой хотите узнать подробнее:", reply_markup=keyboard)
        else:
            send_subscription_request(bot, user_id)

    @bot.message_handler(func=lambda message: message.text in ["🟢 ЭП20003 — 2 метра", "🔵 ЭП40003 — 4 метра", "🟠 ЭП60003 — 6 метров"])
    def handle_buttons(message):
        global caption, media
        user_id = message.from_user.id

        sent_message = bot.send_message(user_id, "Сейчас отправлю фото...", reply_markup=ReplyKeyboardRemove())

        if message.text == "🟢 ЭП20003 — 2 метра":
            caption = r"""
    🔹 **Модель: ЭП20003**  
    📏 **Высота подъёма:** 2 метра  

    🔥 **Ключевые преимущества:**  

    ✅ **Максимальная доступная высота**  
    \- Подъём площадки на **2 метра** позволяет работать на высоте **до 4 метров** \(с учётом роста человека\)\.  
    \- Отлично подходит для **внутренней отделки, монтажа потолков, электропроводки, ремонта складов** и других задач\.  

    ✅ **Компактность и мобильность**  
    \- **Проезжает** в стандартные дверные проёмы шириной **700 мм** \(в сложенном состоянии\)\.  
    \- 📦 **Габариты в опущенном положении:**  
      \- **Высота подъёмника:** 1650 мм \(удобно для транспортировки\)\.  
      \- **Высота площадки:** 324 мм \(низкий старт для быстрого размещения\)\.  

    ✅ **Быстрый запуск**  
    \- 🔧 **Готов к работе без сборки\!**  
    \- **Достаточно:**  
      1️⃣ Разложить стойки и ограждение\.  
      2️⃣ Зафиксировать несколько винтов \(инструменты в комплекте\)\.  
    \- ⏳ **Время подготовки:** менее **10 минут**\.  

    ✅ **Надёжность и безопасность**  
    \- 🏋 **Грузоподъёмность:** **300 кг** \(2 человека \+ инструмент\)\.  
    \- 🔒 **Противоскользящее покрытие площадки\.**  
    \- 🛑 **Автоматическая блокировка при потере натяжения троса\.**  
    \- ✅ **Сертификат соответствия и допуск для работы людей\.**  
    \- ⚙ **Автоматическая остановка площадки в крайних положениях\.**  

    \-\-\-  

    🎯 **Кому подойдёт\?**  
    🏠 **Строительные бригады:** ремонт квартир, офисов, торговых помещений\.  
    📦 **Складские комплексы:** разгрузка, монтаж стеллажей, обслуживание высотных зон\.  
    🏭 **Промышленные предприятия:** монтаж оборудования, покраска, обслуживание коммуникаций\.  

    \-\-\-  

    ❓ **Почему стоит выбрать ЭП20003\?**  
    ⏳ **Экономия времени:** без лишней сборки – сразу к работе\!  
    💰 **Без аренды:** покупаете оборудование, а не платите за временное использование\.  
    🇷🇺 **Российское производство:** доступные запчасти и сервисная поддержка\. """

            media = [
                InputMediaPhoto(open("images/el2m_ph.jpg", "rb")),
                InputMediaPhoto(open("images/all_el_ch.jpg", "rb")),
            ]
        elif message.text == "🔵 ЭП40003 — 4 метра":
            caption = escape_markdown_v2("""

    **Модель: ЭП40003**  
    🔹 **Ключевые преимущества:**  

    ✅ **Работа на высоте до 6 метров** – стоя на площадке, рабочий легко выполняет задачи на высоте **4–6 метров**.  
    ✅ **Грузоподъёмность 300 кг** – выдерживает **инструменты, материалы и 1–2 человек** одновременно.  
    ✅ **Быстрая сборка** – стойки и ограждение устанавливаются **за 15 минут**, полная настройка – **10 минут**.  
    ✅ **Максимальная безопасность** – защита от падений, аварийные механизмы.  

    ---  

    🔒 **Системы безопасности:**  

    1️⃣ **Автоматическое отключение в крайних положениях**  
       - 🔹 Концевые выключатели останавливают подъём при достижении **верхней/нижней точки**.  

    2️⃣ **Автоматическая блокировка при потере натяжения троса**  
       - 🔹 Площадка мгновенно **фиксируется**, исключая потерю равновесия.  

    3️⃣ **Противоскользящее покрытие**  
       - 🔹 Специальное **рифлёное покрытие** платформы для уверенной работы.  

    ---  

    🚀 **Преимущества для вашего бизнеса:**  

    🔹 **Готовность к работе «из коробки»** – оборудование поставляется **в полной комплектации**, не требует дополнительных элементов.  
    🔹 **Экономия времени** – установка занимает **15 минут** вместо **часовой сборки аналогов**.  
    🔹 **Снижение рисков** – безопасность рабочих + отсутствие простоев из-за поломок.  

    ---  

    🏗 **Где применяется?**  

    🏠 **Отделка фасадов, монтаж рекламных конструкций**  
    🏗 **Кровельные работы, установка окон и вентиляции**  
    📦 **Ремонт складских помещений, ангаров, торговых центров**  

    ---  

    🔥 **Почему выбирают нас?**  

    🇷🇺 **Российское производство** – оперативные поставки, ремонт и замена запчастей.  
    🛠 **Гарантия 1 год + техническая поддержка** – всегда поможем решить вопросы.  
    🎓 **Обучение сотрудников** – проводим инструктаж по работе с оборудованием.""")

            media = [
                InputMediaPhoto(open("images/el4m_ph.jpg", "rb")),
                InputMediaPhoto(open("images/all_el_ch.jpg", "rb")),
            ]
        elif message.text == "🟠 ЭП60003 — 6 метров":
            caption = escape_markdown_v2("""
    **Модель: ЭП60003**  

    🔹 **Основные характеристики:**  
    - 📏 **Высота подъёма:** **6 метров**  
    - 🛠 **Рабочая зона:** Стоя на площадке, человек может дотянуться **до 8 метров**  
    - 🏋 **Грузоподъёмность:** **до 300 кг** (оборудование + материалы + работник)  
    - ⚡ **Сборка:** Полностью готовый комплект  
      - **Установка стоек и ограждения** — **30 минут**  
      - **Настройка оборудования** — **10 минут**  

    ---  

    ✅ **Ключевые преимущества:**  

    🔒 **1. Безопасность:**  
    - 🛑 **Автоматическое отключение в крайних положениях** (концевые выключатели)  
    - 🔗 **Блокирующий механизм при потере натяжения троса** – площадка мгновенно фиксируется  
    - 🔩 **Дополнительные укосины** обеспечивают устойчивость даже на максимальной высоте  
    - 🚧 **Противоскользящее покрытие** на платформе и ступенях  

    🚀 **2. Мобильность и удобство:**  
    - 🔄 **Колёса с фиксаторами** – перемещение **одним человеком**  
    - ⏳ **Быстрая установка** – **менее 40 минут** до полной готовности  
    - 📦 **Компактность** – удобное хранение, не занимает много места  

    🔧 **3. Надёжность:**  
    - 🇷🇺 **Российское производство** – адаптировано к местным условиям и стандартам  
    - 📜 **Сертифицировано** – допуск для работы людей  

    ---  

    🔍 **Как это работает?**  
    1️⃣ **Установите стойки и ограждение** (**30 минут**)  
    2️⃣ **Настройте оборудование**, подтянув и зафиксировав трос (**10 минут**)  
    3️⃣ **Готово!** Поднимайтесь, работайте, перемещайтесь — **управляйте платформой дистанционно с радиопульта!** 🎮  

    ---  

    🎯 **Для каких задач подходит?**  
    🏢 **Отделка фасадов, монтаж конструкций, ремонт высотных зданий**  
    🔌 **Работа с коммуникациями** (электропроводка, вентиляция)  
    📦 **Погрузочно-разгрузочные работы** на складах  

    ---  

    🔥 **Почему выбирают нас?**  
    ⏳ **Экономия времени** – минимальная подготовка **→ максимум эффективности**  
    🛑 **Без простоев** – автоматика предотвращает поломки и аварии  
    💰 **Выгода** – снижение затрат на аренду сложной техники""")

            media = [
                InputMediaPhoto(open("images/el6m_ph.jpg", "rb")),
                InputMediaPhoto(open("images/all_el_ch.jpg", "rb")),
            ]

        # Отправляем сообщение и убираем клавиатуру
        bot.send_media_group(user_id, media)
        bot.send_message(user_id, caption, parse_mode="MarkdownV2")
        bot.delete_message(user_id, sent_message.message_id)

    @bot.message_handler(commands=['contact'])
    def contact_us(message):
        user_id = message.from_user.id
        if check_user_subscription(bot, user_id):
            bot.send_message(user_id,
                             "Чтобы наш менеджер вам позвонил, пожалуйста, напишите свой номер телефона и почту в одном сообщении.")
            bot.register_next_step_handler(message, get_user_contacts)
        else:
            send_subscription_request(bot, user_id)

    def get_user_contacts(message):
        user_id = message.from_user.id
        user_contacts = message.text
        for admin in ADMINS:
            bot.send_message(admin, user_contacts)
            bot.send_message(admin, "У вас новый человек, который оставил свой номер телефона и почту!")
        bot.send_message(user_id,
                         "С радостью сообщаем вам, что ваши контактные данные были отправлены нашему менеджеру. В ближайшее время он свяжется с вами.")

