from config import bot, updateId
from reg import start
from SQLite import botStart, registration
from isLogged import menu


@bot.message_handler(commands=['start'])
def welcome(message):
    user_id = updateId(message)
    print(user_id)
    botStart()
    if registration(user_id):
        start(message)
    else:
        bot.send_message(message.from_user.id, "Рады видеть тебя вновь")
        menu(message)


bot.polling()
