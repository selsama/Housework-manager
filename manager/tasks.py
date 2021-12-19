from db import db

def create(holdID, name, description):
    try:
        sql = "INSERT INTO tasks (name, description, householdid) VALUES (:name, :description, :householdID)"
        db.session.execute(sql, {"name":name, "description":description, "householdID":holdID})
        sql = "SELECT MAX(id) FROM tasks"
        id = db.session.execute(sql).fetchone()
        db.session.commit()
        return id.max
    except:
        print("error in creating task")
        db.session.rollback()
        return False

def getTasks(holdID):
    sql = "SELECT * FROM tasks WHERE householdid=:holdID"
    result = db.session.execute(sql, {"holdID":holdID})
    return result.fetchall()

def getTask(taskID):
    sql = "SELECT * FROM tasks WHERE id=:id"
    result = db.session.execute(sql, {"id":taskID})
    return result.fetchone()

def editTask(taskID, name, description):
    sql = "UPDATE tasks SET name=:name, description=:desc WHERE id=:id"
    db.session.execute(sql, {"id":taskID, "name":name, "desc":description})
    db.session.commit()

def deleteTask(taskID):
    sql = "DELETE FROM tasks WHERE id=:id"
    db.session.execute(sql, {"id":taskID})
    db.session.commit()