from sqlalchemy.sql.elements import Null
from app import app
from flask import abort, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

import users
import households
import tasks

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
    if not session["userID"]:
        return render_template("myHouseholds.html")
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
    return redirect("/myHouseholds")

@app.route("/household<int:id>")
def household(id):
    name = households.getName(id)
    tasks = households.getTasks(id)
    contributors = households.getContributors(id)
    admin = households.isAdmin(session["userID"], id)
    return render_template("household.html", id=id, name=name, tasks=tasks, contributors=contributors, admin=admin, last = (len(contributors) == 1))

@app.route("/household<int:id>/options")
def householdOptions(id):
    name = households.getName(id)
    contributors = households.getContributors(id)
    admin = households.isAdmin(session["userID"], id)
    return render_template("householdOptions.html", id=id, name=name, contributors=contributors, admin=admin)

@app.route("/household<int:id>/edit", methods=["POST"])
def householdEdit(id):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if request.form["action"] == "add":
        user = users.userID(request.form["username"])
        if request.form.get("admin"):
            admin = True
        else:
            admin = False
        if user == -1:
            pass
        else:
            households.giveRights(id, user, admin)
    if request.form["action"] == "admin":
        userID = request.form["user"]
        if request.form.get("admin"):
            admin = True
        else:
            admin = False
        households.updateRights(id, userID, admin)
    if request.form["action"] == "remove":
        user = request.form["user"]
        households.removeUser(user, id)
    if request.form["action"] == "rename":
        name = request.form["name"]
        households.rename(id, name)
    if request.form["action"] == "leave":
        admin = households.isAdmin(session["userID"], id)
        households.removeUser(session["userID"], id)
        if admin:
            households.reactToAdminLeaving(id)
        return redirect("/myHouseholds")
    return redirect("/household" + str(id) + "/options")

@app.route("/household<int:id>/createTask")
def createTask(id):
    name = households.getName(id)
    return render_template("createTask.html", holdID=id, holdName=name)

@app.route("/household<int:id>/newTask", methods=["POST"])
def newTask(id):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    name = request.form["name"]
    desc = request.form["description"]
    date = request.form["deadline"]
    households.createTask(id, name, desc, date)
    return redirect("/household" + str(id))

@app.route("/household<int:holdID>/task<int:taskID>")
def task(holdID, taskID):
    task = tasks.getTask(taskID)
    assignees = tasks.getAssignees(taskID)
    return render_template("task.html", holdID=holdID, task=task, assignees=assignees)

@app.route("/household<int:holdID>/editTask<int:taskID>", methods=["POST"])
def editTask(holdID, taskID):
    if request.form["edit"] == "start":
        pass
    elif request.form["edit"] == "stop":
        return redirect("/household" + str(holdID) + "/task" + str(taskID))
    elif request.form["edit"] == "delete":
        tasks.deleteTask(taskID)
        return redirect("/household" + str(holdID))
    elif request.form["edit"] == "save":
        name = request.form["name"]
        desc = request.form["description"]
        if request.form.get("complete"):
            complete = True
        else:
            complete = False
        tasks.editTask(taskID, name, desc, complete)
        tasks.setDeadline(taskID, request.form["deadline"])
        if request.form.get("assigned"):
            tasks.assign(taskID, session["userID"])
        else:
            tasks.deassign(taskID, session["userID"])
    task = tasks.getTask(taskID)
    assignees = tasks.getAssignees(taskID)
    mine = tasks.isAssigned(session["userID"], taskID)
    return render_template("editTask.html", holdID=holdID, task=task, assignees=assignees, mine=mine)