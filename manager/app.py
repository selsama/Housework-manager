from flask import Flask
from flask import redirect, render_template, request, session
from os import getenv


app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    # check password
    session["username"] = username
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/myHouseholds", methods=["POST"])
def myHouseholds():
    return render_template("myHouseholds.html", name = request.form["name"])
