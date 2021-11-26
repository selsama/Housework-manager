from app import app
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

import users

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    users.login(username, password)
    return redirect("/")

@app.route("/register")
def register():
    return render_template("signup.html")

@app.route("/signup", methods=["POST"])
def signup():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    users.register(username, password1, password2)
    return redirect("/")


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")


@app.route("/myHouseholds", methods=["POST"])
def myHouseholds():
    return render_template("myHouseholds.html", name = request.form["name"])
