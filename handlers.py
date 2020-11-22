from telebot import types
from config import bot, updateId, updateUsername
from SQLite import doTaskSQL, offerTaskSQL, userInfoSQL, SQLreg

section = ''
subject = ''
difficulty = ''
money = ''
name = ''
age, course = 0, 0


def mainMenu(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyButton = types.InlineKeyboardButton(text="Выполнить задание")
    keyboard.add(keyButton)
    keyButton = types.InlineKeyboardButton(text="Дать задание")
    keyboard.add(keyButton)
    keyButton = types.InlineKeyboardButton(text="Информация о профиле")
    keyboard.add(keyButton)
    keyButton = types.InlineKeyboardButton(text="Сообщения")
    keyboard.add(keyButton)
    bot.send_message(message.from_user.id, "Выбирай", reply_markup=keyboard)


def doTask(message):
    global section
    section = message.text
    keyboard = types.ReplyKeyboardMarkup()
    key_firstBestLesson = types.InlineKeyboardButton(text="Математика")
    keyboard.add(key_firstBestLesson)
    key_secondBestLesson = types.InlineKeyboardButton(text="Информатика")
    keyboard.add(key_secondBestLesson)
    key_anotherLesson = types.InlineKeyboardButton(text="Физика")
    keyboard.add(key_anotherLesson)
    key_next = types.InlineKeyboardButton(text="Далее")
    keyboard.add(key_next)

    bot.send_message(message.from_user.id, "Выбери предмет", reply_markup=keyboard)

    bot.register_next_step_handler(message, taskDifficulty)


def taskDifficulty(message):
    global subject
    subject = message.text

    keyboard = types.ReplyKeyboardMarkup()
    keyButton = types.InlineKeyboardButton(text="Легкая")
    keyboard.add(keyButton)
    keyButton = types.InlineKeyboardButton(text="Средняя")
    keyboard.add(keyButton)
    keyButton = types.InlineKeyboardButton(text="Сложная")
    keyboard.add(keyButton)

    bot.send_message(message.from_user.id, "Выбери сложность задания", reply_markup=keyboard)
    global section
    if section == "Выполнить задание":
        bot.register_next_step_handler(message, chooseTask)
    elif section == "Дать задание":
        bot.register_next_step_handler(message, giveTask)


def chooseTask(message):
    global difficulty, subject, money
    difficulty = message.text
    money = doTaskSQL(subject, difficulty)
    keyboard = types.InlineKeyboardMarkup()
    if len(money) == 0:
        bot.send_message(message.from_user.id, "К сожалению, заданий нет по выбранным критериям нет",
                         reply_markup=keyboard)
        mainMenu(message)
    else:
        for i in money:
            keyButton = types.InlineKeyboardButton(text=str(i[0]), url="https://vk.com/d.reva99")
            keyboard.add(keyButton)
        keyboard = types.ReplyKeyboardMarkup()
        keyButton = types.InlineKeyboardButton(text="Вернуться к главному меню")
        keyboard.add(keyButton)

        bot.send_message(message.from_user.id, "Выбери задание", reply_markup=keyboard)
        bot.register_next_step_handler(message, mainMenu)


def giveTask(message):
    global difficulty
    difficulty = message.text
    bot.send_message(message.from_user.id, "Сколько заплатишь за выполнение?")
    bot.register_next_step_handler(message, giveMoney)


def giveMoney(message):
    global money, subject, difficulty, user_id
    user_id = updateId(message)
    money = int(message.text)
    offerTaskSQL(user_id, subject, difficulty, money)
    mainMenu(message)


def userInfo(message, user_id):
    information = userInfoSQL(user_id)
    name = information[0][0]
    age = information[1][0]
    course = information[2][0]
    money = information[3][0]
    bot.send_message(message.from_user.id,
                     "Получается, тебя зовут " + name + "\nТвой возраст: " + str(age) +
                     "\nТы учишься на " + str(course) + " курсе\nИ на твоем счету" + str(money))
    keyboard = types.ReplyKeyboardMarkup()
    keyButton = types.InlineKeyboardButton(text="Да")
    keyboard.add(keyButton)
    keyButton = types.InlineKeyboardButton(text="Нет")
    keyboard.add(keyButton)
    bot.send_message(message.from_user.id, text="Все верно?", reply_markup=keyboard)
    bot.register_next_step_handler(message, answer)


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
        bot.register_next_step_handler(message, result)


def result(message):
    bot.send_message(message.from_user.id,
                     "Получается, тебя зовут " + name + "\nТвой возраст: " + str(age) +
                     "\nТы учишься на " + str(course) + " курсе")
    keyboard = types.ReplyKeyboardMarkup()
    keyButton = types.InlineKeyboardButton(text="Да")
    keyboard.add(keyButton)
    keyButton = types.InlineKeyboardButton(text="Нет")
    keyboard.add(keyButton)
    bot.send_message(message.from_user.id, text="Все верно?", reply_markup=keyboard)
    bot.register_next_step_handler(message, answer)


def answer(message):
    if message.text == "Да":
        user_id = updateId(message)
        user_username = updateUsername(message)
        SQLreg(user_id, name, user_username, age, course)
        bot.send_message(message.from_user.id, "Приятно познакомиться")
        mainMenu(message)

    elif message.text == "Нет":
        bot.send_message(message.from_user.id, "Давай попробуем еще раз!\nКак тебя зовут?")
        bot.register_next_step_handler(message, name_register)
