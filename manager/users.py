from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
import secrets

def login(username, password):
    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        print("couldn't find username")
        return False
    else:
        if check_password_hash(user.password, password):
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return True
        else:
            print("incorrect password")
            return False

def logout():
    del session["username"]

def register(username, password1, password2, nickname):
    if password1 != password2:
        return False
    hash_value = generate_password_hash(password1)
    try:
        sql = "INSERT INTO users (username,password,nickname) VALUES (:username,:password,:nickname)"
        db.session.execute(sql, {"username":username, "password":hash_value, "nickname":nickname})
        db.session.commit()
        return True
    except:
        print("error in registrating new user")
        return False
    
def deleteUser(password):
    sql = "SELECT password, id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username()})
    user = result.fetchone()
    if not user:
        print("couldn't find username")
        return False
    else:
        if check_password_hash(user.password, password):
            sql = "DELETE FROM users WHERE id=:id"
            db.session.execute(sql, {"id":user.id})
            db.session.commit()
            logout()
            return True
        else:
            print("incorrect password")
            return False


def username():
    return session.get("username")