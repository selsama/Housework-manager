from db import db


def create(name):  
    try:
        sql = "INSERT INTO households (name) VALUES (:name)"
        db.session.execute(sql, {"name":name})
        db.session.commit()
        return True
    except:
        print("error in creating household")
        return False

def getHouseholds():
    sql = "SELECT * FROM households"
    result = db.session.execute(sql)
    return result.fetchall()
