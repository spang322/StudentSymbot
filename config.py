import telebot


TOKEN = "1431032404:AAGS9MagsZ9mVTKGk9rluaAYpdOA-ZQOQ_M"
bot = telebot.TeleBot(TOKEN)

def updateId(message):
    return message.from_user.id