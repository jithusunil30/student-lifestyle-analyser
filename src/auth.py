import sqlite3

def create_user_table():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT,
            password TEXT
        )
    """)

    conn.commit()
    conn.close()


def register_user(username, password):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=?", (username,))
    if c.fetchone():
        return False

    c.execute("INSERT INTO users VALUES (?,?)", (username, password))
    conn.commit()
    conn.close()
    return True


def login_user(username, password):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = c.fetchone()

    conn.close()
    return result is not None