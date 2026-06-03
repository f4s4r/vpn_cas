from flask import Flask, render_template, request, redirect
import sqlite3
import hashlib

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        db = sqlite3.connect("users.sqlite")
        db.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
        db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password_hash))
        db.commit()
        db.close()
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        db = sqlite3.connect("users.sqlite")
        cur = db.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password_hash))
        row = cur.fetchone()
        db.close()
        if row:
            return render_template("success.html", username=username)
        return render_template("login.html", error="wrong username or password")
    return render_template("login.html")

app.run(host="0.0.0.0", port=5000)
