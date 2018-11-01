from flask import Flask,render_template,request,session,url_for,redirect
from cs50 import SQL
from flask_session import Session

app = Flask(__name__)

db = SQL("sqlite:///books.db")

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/register",methods=["POST","GET"])
def register():
    result = db.execute("INSERT INTO users(username,password)\
                        VALUES(:username,:password)",\
                        username = request.form.get("username"),password = request.form.get("password"))

    return "Registered Successfuly"

@app.route("/login",methods=["POST","GET"])
def login():
        # ensure username was submitted
        if not request.form.get("username"):
            message="Must provide username"
            return render_template("success.html",message=message)

        # ensure password was submitted
        elif not request.form.get("password"):
            message="Must provide password"
            return render_template("success.html",message=message)

        # query database for username 
        rows = db.execute("SELECT * FROM users \
                           WHERE username = :username and password = :password", \
                           username=request.form.get("username"),password=request.form.get("password"))

        # ensure username exists and password is correct
        if len(rows) != 1:
            message="invalid username and/or password"
            return render_template("success.html",message=message)

        message="login successful"
        return render_template("success.html",message=message)
            