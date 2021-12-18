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
    return render_template("options.html", nick=users.nickname())

@app.route("/delete", methods=["POST"])
def delete():
    password = request.form["password"]
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    users.deleteUser(password)
    return redirect("/")

@app.route("/edit", methods=["POST"])
def edit():
    nick = request.form["nickname"]
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    users.changeNickname(nick)
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
    contributors = households.getContributors(id)
    admin = households.isAdmin(session["userID"], id)
    return render_template("household.html", id=id, name=name, tasks=tasks, contributors=contributors, admin=admin)

@app.route("/household<int:id>/options")
def householdOptions(id):
    name = households.getName(id)
    contributors = households.getContributors(id)
    return render_template("householdOptions.html", id=id, name=name, contributors=contributors)

@app.route("/household<int:id>/edit", methods=["POST"])
def householdEdit(id):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if request.form["action"] == "add":
        user = users.userID(request.form["username"])
        if user == -1:
            # TODO: give error message
            return
        else:
            households.giveRights(id, user, True)
    if request.form["action"] == "admin":
        nick = request.form["nick"]
        if request.form.get("admin"):
            admin = True
        else:
            admin = False
        households.updateRights(id, nick, admin)
    if request.form["action"] == "remove":
        nick = request.form["nick"]
        households.removeUser(nick, id)
    if request.form["action"] == "rename":
        name = request.form["name"]
        households.rename(id, name)
    return redirect("/household" + str(id) + "/options")

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