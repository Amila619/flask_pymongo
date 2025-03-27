from flask import Flask, request
from pydantic import ValidationError
from database import get_db
from schemas import User
from bson import json_util, ObjectId
import json, valkey
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

valkey_uri = os.getenv('RURI')
valkey_client = valkey.from_url(valkey_uri)

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
    u_id = json.loads(json_util.dumps(u_id))["$oid"]
    valkey_client.set('f_id', u_id, ex=300)
    return{"id" : u_id, "message" : "Successfully inserted User"}, 201

@app.route("/user", methods = ["GET"])
def get_user():
    db = get_db()
    try:
        u_id = valkey_client.get('f_id').decode('utf-8')
        user = db.users.find_one({"_id": ObjectId(u_id)})
    except:
        return {"message": "Invalid user ID"}, 400
    
    del user['_id']
    return {"data" : user}, 200

if __name__ == "__main__":
    app.run(debug=True)