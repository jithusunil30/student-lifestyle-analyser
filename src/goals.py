import sqlite3

def create_goal_table():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            username TEXT,
            target_score REAL
        )
    """)

    conn.commit()
    conn.close()


def set_goal(username, target):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("DELETE FROM goals WHERE username=?", (username,))
    c.execute("INSERT INTO goals VALUES (?,?)", (username, target))

    conn.commit()
    conn.close()


def get_goal(username):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT target_score FROM goals WHERE username=?", (username,))
    result = c.fetchone()

    conn.close()
    return result[0] if result else None