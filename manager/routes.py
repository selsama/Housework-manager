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

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

# @app.route("signup")
# def signup():


@app.route("/myHouseholds", methods=["POST"])
def myHouseholds():
    return render_template("myHouseholds.html", name = request.form["name"])
