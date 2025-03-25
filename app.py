from flask import Flask, request, redirect, session
from pydantic import ValidationError
from database import get_db
from schemas import User
from datetime import timedelta
import secrets

app = Flask(__name__)

app.secret_key = secrets.token_hex(32)
app.config['SESSION_PERMANENT'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)

@app.route("/")
def root():
    return "<h1>Mongo DB + Flask</h1>"

@app.route("/register", methods = ["POST"])
def register_user():
    db = get_db()
    try:
        data = request.form.to_dict()
        user = User(**data)
    except ValidationError as error:
        e = error.errors()[0]
        return {"error" :{"type" : e["type"], "loc" : e["loc"], "msg" : e["msg"]}}, 400
    u_id = db.users.insert_one(user.model_dump()).inserted_id
    session['f_id'] = u_id
    return{"id" : str(u_id), "message" : "Successfully inserted User"}, 201

@app.route("/user", methods = ["GET"])
def get_user():
    if 'f_id' not in session:
        return {"data" : "Nothing to return"}, 401

    db = get_db()
    u_id = session['f_id']
    user = db.users.find_one({"_id": u_id})
    if not user:
        return {"message" : "user does not exist"}, 404
    del user['_id']
    return {"data" : user}, 200

if __name__ == "__main__":
    app.run(debug=True)