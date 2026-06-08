from flask import Flask, render_template, request, redirect
import hashlib
import db

db.init_db()

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
        db.register(username, password_hash)
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if db.login(username, password_hash):
            return render_template("success.html", username=username)
        return render_template("login.html", error="wrong username or password")
    return render_template("login.html")

app.run(host="0.0.0.0", port=5000)
