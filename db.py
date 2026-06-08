import sqlite3

def connect():
    return sqlite3.connect("users.sqlite")

def init_db():
    db = connect()
    db.execute("CREATE TABLE IF NOT EXISTS roles (id INTEGER PRIMARY KEY, name TEXT)")
    db.execute("CREATE TABLE IF NOT EXISTS permissions (id INTEGER PRIMARY KEY, name TEXT)")
    db.execute("CREATE TABLE IF NOT EXISTS role_permissions (role_id INTEGER, permission_id INTEGER)")
    db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role_id INTEGER)")
    db.commit()

    count = db.execute("SELECT COUNT(*) FROM roles").fetchone()[0]
    if count == 0:
        db.execute("INSERT INTO roles (id, name) VALUES (1, 'admin')")
        db.execute("INSERT INTO roles (id, name) VALUES (2, 'user')")
        db.execute("INSERT INTO permissions (id, name) VALUES (1, 'connect')")
        db.execute("INSERT INTO role_permissions (role_id, permission_id) VALUES (1, 1)")
        db.execute("INSERT INTO role_permissions (role_id, permission_id) VALUES (2, 1)")
        db.commit()
    db.close()

def register(username, password):
    db = connect()
    db.execute("INSERT INTO users (username, password, role_id) VALUES (?, ?, 2)", (username, password))
    db.commit()
    db.close()

def login(username, password):
    db = connect()
    cur = db.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    row = cur.fetchone()
    db.close()
    return row is not None

def has_permission(username, permission_name):
    db = connect()
    query = "SELECT permissions.name FROM users JOIN role_permissions ON users.role_id = role_permissions.role_id JOIN permissions ON role_permissions.permission_id = permissions.id WHERE users.username = ? AND permissions.name = ?"
    cur = db.execute(query, (username, permission_name))
    row = cur.fetchone()
    db.close()
    return row is not None
