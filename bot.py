import telebot

#token:1337741156:AAEAXiceoDUDxtQloBS1L3_rYp9SpWUnhc

name = ''
age = 0
course = 0
skills = ''
trabls = ''


bot = telebot.TeleBot("1337741156:AAEAXiceoDUDxtQloBS1L3_rYp9SpWUnhc")

@bot.message_handler(commands=['start'])
def register(message):
	bot.reply_to(message, "Привет, как тебя зовут?")
	def name(message):
		name = message.text
		bot.reply_to(message, "Сколько вам лет")
