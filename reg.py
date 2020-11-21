# token:1337741156:AAEAXiceoDUDxtQloBS1L3_rYp9SpWUnhc
# token:1431032404:AAFL8WHpn2dJryplX4Bc5oUA3iiWj9WjfqA
from telebot import types
from config import bot, updateId
from isLogged import menu
from SQLite import SQLreg


#@bot.message_handler(func=lambda m: True, content_types=['text'])
def start(message):
    bot.send_message(message.from_user.id, "Привет, как тебя зовут?")
    bot.register_next_step_handler(message, name_register)


def name_register(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, "Окей, сколько тебе лет?")
    bot.register_next_step_handler(message, age_reg)


def age_reg(message):
    global age
    while True:
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
    while True:
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
        user_id = updateId(message)
        print(user_id)
        SQLreg(user_id, name, skills, lowSkills, age, course)
        menu(message)
        bot.send_message(message.from_user.id, "Приятно познакомиться, я записал тебя в БД :)")

    elif message.text == "Нет":
        bot.send_message(message.from_user.id, "Давай попробуем еще раз!")
        bot.send_message(message.from_user.id, "Как тебя зовут ?")
        bot.register_next_step_handler(message, name_register)
