import sqlite3

def init_db():
    db = sqlite3.connect("users.sqlite")
    db.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    db.commit()
    db.close()

def register(username, password):
    db = sqlite3.connect("users.sqlite")
    db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    db.commit()
    db.close()

def login(username, password):
    db = sqlite3.connect("users.sqlite")
    cur = db.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    row = cur.fetchone()
    db.close()
    return row is not None
