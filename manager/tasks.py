from db import db

def create(holdID, name, description, deadline):
    try:
        sql = "INSERT INTO tasks (name, description, householdid) VALUES (:name, :description, :householdID)"
        db.session.execute(sql, {"name":name, "description":description, "householdID":holdID})
        sql = "SELECT MAX(id) FROM tasks"
        id = db.session.execute(sql).fetchone()
        db.session.commit()
        setDeadline(id.max, deadline)
        return id.max
    except:
        print("error in creating task")
        db.session.rollback()
        return False

def getTasks(holdID):
    sql = "SELECT * FROM tasks WHERE householdid=:holdID ORDER BY deadline"
    result = db.session.execute(sql, {"holdID":holdID})
    return result.fetchall()

def getTask(taskID):
    sql = "SELECT * FROM tasks WHERE id=:id"
    result = db.session.execute(sql, {"id":taskID})
    return result.fetchone()

def editTask(taskID, name, description, complete):
    sql = "UPDATE tasks SET name=:name, description=:desc, complete=:complete WHERE id=:id"
    db.session.execute(sql, {"id":taskID, "name":name, "desc":description, "complete":complete})
    db.session.commit()

def setDeadline(taskID, date):
    if not date:
        sql = "UPDATE tasks SET deadline=null WHERE id=:id"
        db.session.execute(sql, {"id":taskID})
    else:
        sql = "UPDATE tasks SET deadline=TO_DATE(:date, 'YYYY-MM-DD') WHERE id=:id"
        db.session.execute(sql, {"id":taskID, "date":date})
    db.session.commit()

def deleteTask(taskID):
    sql = "DELETE FROM tasks WHERE id=:id"
    db.session.execute(sql, {"id":taskID})
    db.session.commit()

def getAssignees(taskID):
    sql = "SELECT u.id, u.nickname FROM users u, assignees a WHERE a.taskid=:id AND u.id=a.userid"
    result = db.session.execute(sql, {"id":taskID})
    return result.fetchall()

def assign(taskID, userID):
    if isAssigned(userID, taskID):
        return
    sql = "INSERT INTO assignees (userid, taskid) VALUES (:user, :task)"
    db.session.execute(sql, {"user":userID, "task":taskID})
    db.session.commit()

def deassign(taskID, userID):
    if not isAssigned(userID, taskID):
        return
    sql = "DELETE FROM assignees WHERE userid=:user AND taskid=:task"
    db.session.execute(sql, {"user":userID, "task":taskID})
    db.session.commit()

def setAssignees(taskID):
    return

def isAssigned(userID, taskID):
    sql = " SELECT 1 FROM assignees WHERE userid=:userID AND taskID=:taskID"
    result = db.session.execute(sql, {"userID":userID, "taskID":taskID})
    if result.fetchone():
        return True
    return False