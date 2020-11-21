import sqlite3


def createServer():
    global db, sql
    db = sqlite3.connect("server.db")
    sql = db.cursor()

    sql.execute("""CREATE TABLE IF NOT EXISTS users (
                    login TEXT,
                    password TEXT,
                    id TEXT
                )""")

    db.commit()


def reg():

    user_id = input()

    sql.execute(f"SELECT id FROM users WHERE login = ?", user_id)
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO users VALUES (?)", (user_id))
        db.commit()

        print("Зарегистрировано")
    else:
        print("Уже есть")

        for value in sql.execute("SELECT * FROM users"):
            print(value[0])


def bot():
    createServer()


bot()
