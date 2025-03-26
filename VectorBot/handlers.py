from telebot import TeleBot

def register_handlers(bot: TeleBot):

    @bot.message_handler(commands=["start"])
    def welcome_script(message):
        user_id = message.from_user.id
        bot.send_message(user_id, f"Здравствуйте, {message.from_user.first_name}! \nЭтот бот поможет ")
