from app import app
from flask import abort, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

import users
import households

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    users.login(username, password)
    # TODO: Find out how to return the page the user was at after login
    return redirect("/")

@app.route("/register")
def register():
    return render_template("signup.html")

@app.route("/signup", methods=["POST"])
def signup():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    nickname = request.form["nickname"]
    users.register(username, password1, password2, nickname)
    return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/options")
def options():
    return render_template("options.html")

@app.route("/delete", methods=["POST"])
def delete():
    password = request.form["password"]
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    users.deleteUser(password)
    return redirect("/")

@app.route("/myHouseholds")
def myHouseholds():
    list = households.getHouseholds(session["userID"])
    return render_template("myHouseholds.html", households=list)

@app.route("/createHousehold")
def createHousehold():
    return render_template("createHousehold.html")

@app.route("/new", methods=["POST"])
def new():
    name = request.form["name"]
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    households.create(name, session["userID"])
    return redirect("/myHouseholds") # TODO: direct to the household instead

@app.route("/household<int:id>")
def household(id):
    name = households.getName(id)
    tasks = households.getTasks(id)
    return render_template("household.html", id=id, name=name, tasks = tasks)

@app.route("/household<int:id>/createTask")
def createTask(id):
    name = households.getName(id)
    return render_template("createTask.html", holdID = id, holdName = name)

@app.route("/household<int:id>/newTask", methods=["POST"])
def newTask(id):
    name = request.form["name"]
    desc = request.form["desc"]
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    households.createTask(id, name, desc)
    return redirect("/household" + str(id)) # TODO: direct to the task instead

# @app.route("/task<int:id>")
# def household(id):
#     name = households.getName(id)
#     return render_template("household.html", id=id, name=name)