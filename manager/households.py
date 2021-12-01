from db import db


def create(name, creator):  
    try:
        sql = "INSERT INTO households (name) VALUES (:name)"
        db.session.execute(sql, {"name":name})
        sql = "SELECT MAX(id) FROM households"
        id = db.session.execute(sql).fetchone()
        sql = "INSERT INTO admins (householdID, userID) VALUES (:houseID, :userID)"
        db.session.execute(sql, {"houseID":id.max, "userID":creator})
        db.session.commit()
        return True
    except:
        print("error in creating household")
        db.session.rollback()
        return False

def getHouseholds(user):
    sql = "SELECT h.* FROM households h, admins a WHERE h.id = a.householdID AND a.userID = :user"
    result = db.session.execute(sql, {"user": user})
    return result.fetchall()

def getName(id):
    sql = "SELECT name FROM households WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone().name