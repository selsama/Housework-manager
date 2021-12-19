from db import db
import tasks

def create(name, creator):  
    try:
        sql = "INSERT INTO households (name) VALUES (:name)"
        db.session.execute(sql, {"name":name})
        sql = "SELECT MAX(id) FROM households"
        id = db.session.execute(sql).fetchone()
        sql = "INSERT INTO access (householdID, userID, admin) VALUES (:houseID, :userID, TRUE)"
        db.session.execute(sql, {"houseID":id.max, "userID":creator})
        db.session.commit()
        return True
    except:
        print("error in creating household")
        db.session.rollback()
        return False

def getHouseholds(user):
    sql = "SELECT h.* FROM households h, access a WHERE h.id = a.householdID AND a.userID = :user"
    result = db.session.execute(sql, {"user": user})
    return result.fetchall()

def getName(id):
    sql = "SELECT name FROM households WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone().name

def createTask(id, name, desc, deadline):
    taskID = tasks.create(id, name, desc, deadline)
    return taskID

def getTasks(id):
    return tasks.getTasks(id)

def giveRights(holdID, userID, admin):
    sql = "SELECT 1 FROM access WHERE householdid=:hold AND userid=:user"
    result = db.session.execute(sql, {"hold": holdID, "user": userID})
    if result.fetchone():
        sql = "UPDATE access SET admin=:admin WHERE householdid=:hold AND userid=:user"
    else:
        sql = "INSERT INTO access (householdid, userid, admin) VALUES (:hold, :user, :admin)"
    db.session.execute(sql, {"hold":holdID, "user":userID, "admin":admin})
    db.session.commit()

def updateRights(holdID, userID, admin):
    sql = "UPDATE access SET admin=:admin WHERE householdid=:hold AND userid=:user"
    db.session.execute(sql, {"hold":holdID, "user":userID, "admin":admin})
    db.session.commit() 

def rename(id, newName):
    sql = "UPDATE households SET name=:new WHERE id=:hold"
    db.session.execute(sql, {"new":newName, "hold":id})
    db.session.commit()

def getContributors(id):
    sql = "SELECT u.id, u.nickname, a.admin FROM access a, users u WHERE a.householdid=:hold AND u.id=a.userid"
    result = db.session.execute(sql, {"hold":id})
    return result.fetchall()

def removeUser(userID, holdID):
    sql = "DELETE FROM access WHERE userid=:user AND householdid=:hold"
    db.session.execute(sql, {"user":userID, "hold":holdID})
    db.session.commit()

def isAdmin(userID, id):
    sql = "SELECT admin FROM access WHERE userid=:user AND householdid=:hold"
    result = db.session.execute(sql, {"user":userID, "hold":id})
    return result.fetchone().admin

def reactToAdminLeaving(id):
    sql = "SELECT 1 FROM access WHERE householdid=:hold AND admin=TRUE"
    result = db.session.execute(sql, {"hold":id})
    if result.fetchone():
        return
    else:
        sql = "SELECT userid FROM access WHERE householdid=:hold"
        result = db.session.execute(sql, {"hold":id})
        user = result.fetchone()
        if user:
            updateRights(id, user.userid, True)
        else:
            deleteHousehold(id)

def deleteHousehold(id):
    sql = "DELETE FROM households WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()

