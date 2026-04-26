import sqlite3
from datetime import datetime

def create_history_table():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS history (
            username TEXT,
            date TEXT,
            sleep REAL,
            study REAL,
            screen REAL,
            exercise REAL,
            diet REAL,
            stress REAL,
            score REAL
        )
    """)

    conn.commit()
    conn.close()


def save_daily_entry(username, data, score):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
        INSERT INTO history VALUES (?,?,?,?,?,?,?,?,?)
    """, (username, datetime.now().strftime("%Y-%m-%d"), *data, score))

    conn.commit()
    conn.close()


def load_user_history(username):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT * FROM history WHERE username=?", (username,))
    rows = c.fetchall()

    conn.close()

    return [
        {
            "date": r[1],
            "sleep": r[2],
            "study": r[3],
            "screen": r[4],
            "exercise": r[5],
            "diet": r[6],
            "stress": r[7],
            "score": r[8],
        }
        for r in rows
    ]