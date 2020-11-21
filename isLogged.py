from telebot import types
from config import bot


#@bot.message_handler(commands=['menu'])
def menu(message):
    keyboard = types.ReplyKeyboardMarkup()
    key_goTask = types.InlineKeyboardButton(text = "Выполнить задание")
    keyboard.add(key_goTask)
    key_addTask = types.InlineKeyboardButton(text = "Дать задание")
    keyboard.add(key_addTask)
    key_information = types.InlineKeyboardButton(text = "Информация о профиле")
    keyboard.add(key_information)
    key_message = types.InlineKeyboardButton(text = "Сообщения")
    keyboard.add(key_message)
    bot.send_message(message.from_user.id, "Выбирай!", reply_markup = keyboard)
