import telebot
from telebot import types

# token:1337741156:AAEAXiceoDUDxtQloBS1L3_rYp9SpWUnhc
name = ''
age = 0
course = 0
skills = ""
lowSkills = ""

bot = telebot.TeleBot("1431032404:AAFL8WHpn2dJryplX4Bc5oUA3iiWj9WjfqA")

print(bot.get_me())

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.from_user.id, "Привет, как тебя зовут ?")


@bot.message_handler(func=lambda m: True, content_types=['text'])
def name_register(message):
    if age == 0:
        global name
        name = message.text
        bot.send_message(message.from_user.id, "Окей, сколько тебе лет?")
        bot.register_next_step_handler(message, age_reg)


def age_reg(message):
    global age
    while age == 0:
        try:
            age = int(message.text)
        except ValueError:

            bot.send_message(message.from_user.id, "Введи цифрами!")
            bot.register_next_step_handler(message, age_reg)
        finally:
            break
    if age != 0:
        bot.send_message(message.from_user.id, "Неплохо, а на каком ты курсе?")
        bot.register_next_step_handler(message, course_reg)


def course_reg(message):
    global course
    while course == 0:
        try:
            course = int(message.text)
        except ValueError:
            bot.send_message(message.from_user.id, "Введи цифрами!")
            bot.register_next_step_handler(message, course_reg)
        finally:
            break
    if course != 0:
        bot.send_message(message.from_user.id, "А что ты умеешь? Опиши вкратце!")
        bot.register_next_step_handler(message, skills_reg)


def skills_reg(message):
    global skills
    skills = message.text
    bot.send_message(message.from_user.id, "Осталось совсем немного) А в чем ты слаб ?")
    bot.register_next_step_handler(message, result)


def result(message):
    global lowSkills
    lowSkills = message.text
    bot.send_message(message.from_user.id,
                     "Получается, тебя зовут " + name + "\nТвой возраст: " + str(age) + "\nТы учишься на " + str(
                         course) + " курсе" + "\nТвоя биография:" + "\n" + skills + "\n" + lowSkills)
    keyboard = types.ReplyKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text="Да")
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text="Нет")
    keyboard.add(key_no)
    bot.send_message(message.from_user.id, text="Все верно ?", reply_markup=keyboard)
    bot.register_next_step_handler(message, answer)


def answer(message):
    if message.text == "Да":
        keyboard = types.ReplyKeyboardMarkup()
        key_menu = types.InlineKeyboardButton(text="/menu")
        keyboard.add(key_menu)
        bot.send_message(message.from_user.id, "Приятно познакомиться, я записал тебя в БД :)")
        bot.send_message(message.from_user.id, "Нажми на кнопку '/menu' для того, чтоб узнать возможности бота!",
                         reply_markup=keyboard)
        bot.stop_polling()

    elif message.text == "Нет":
        global name, skills, lowSkills, age, course
        name, skills, lowSkills = '', '', ''
        age, course = 0, 0
        bot.send_message(message.from_user.id, "Давай попробуем еще раз!")
        bot.send_message(message.from_user.id, "Как тебя зовут ?")
        bot.register_next_step_handler(message, name_register)


bot.polling()