import sqlite3


def createServer():
    global db, sql
    db = sqlite3.connect("server.db", check_same_thread=False)
    sql = db.cursor()
    sql.execute("""CREATE TABLE IF NOT EXISTS users (id INT, name TEXT, age INT,
     course INT, skills TEXT, lowSkills TEXT)""")

    db.commit()


def registration(user_id):
    sql.execute(f"SELECT id FROM users WHERE id = ?", (user_id,))
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", (user_id, '', 0, 0, '', ''))
        db.commit()

        return True
    else:
        return False


def SQLreg(user_id, name, skills, lowSkills, age, course):
    sql.execute(f"UPDATE users SET name = ? WHERE id = ?", (name, user_id))
    sql.execute(f"UPDATE users SET age = ? WHERE id = ?", (age, user_id))
    sql.execute(f"UPDATE users SET course = ? WHERE id = ?", (course, user_id))
    sql.execute(f"UPDATE users SET skills = ? WHERE id = ?", (skills, user_id))
    sql.execute(f"UPDATE users SET lowSkills = ? WHERE id = ?", (lowSkills, user_id))
    db.commit()


def botStart():
    createServer()
