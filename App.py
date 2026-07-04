from flask import Flask, render_template, request, redirect, session
from flask_bcrypt import Bcrypt
import sqlite3

app = Flask(__name__)
app.secret_key = "secretkey"

bcrypt = Bcrypt(app)

def connect_db():
    return sqlite3.connect("database.db")

conn = connect_db()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE,
password TEXT
)
""")
conn.commit()
conn.close()


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/register", methods=["GET","POST"])
def register():

    if request.method=="POST":

        username=request.form["username"]
        password=request.form["password"]

        hashed=bcrypt.generate_password_hash(password).decode("utf-8")

        conn=connect_db()
        cursor=conn.cursor()

        try:
            cursor.execute("INSERT INTO users(username,password) VALUES(?,?)",
            (username,hashed))
            conn.commit()
        except:
            return "User already exists"

        conn.close()

        return redirect("/")

    return render_template("register.html")


@app.route("/login", methods=["POST"])
def check():

    username=request.form["username"]
    password=request.form["password"]

    conn=connect_db()
    cursor=conn.cursor()

    cursor.execute("SELECT password FROM users WHERE username=?",(username,))
    user=cursor.fetchone()

    conn.close()

    if user and bcrypt.check_password_hash(user[0],password):

        session["user"]=username
        return redirect("/home")

    return "Invalid Username or Password"


@app.route("/home")
def home():

    if "user" in session:
        return render_template("home.html",user=session["user"])

    return redirect
