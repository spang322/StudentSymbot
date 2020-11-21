from config import bot, updateId
from reg import start
from SQLite import botStart, registration
from handlers import mainMenu


@bot.message_handler(commands=['start'])
def welcome(message):
    user_id = updateId(message)
    botStart()
    if registration(user_id):
        start(message)
    else:
        bot.send_message(message.from_user.id, "Рады видеть тебя вновь")
        mainMenu(message)


@bot.message_handler(content_types=['text'])
def allMenu(message):
    user_id = updateId(message)
    if message.text == 'Выполнить задание':
        doTask(user_id)


bot.polling()
