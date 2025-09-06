import os

import requests
from faker import Faker
from flask import Flask, request, jsonify
from flask_cors import CORS
from phe import paillier
import allData
import generator
import homomorphicData
import publishedData
import userModels
from extensions import db
app = Flask(__name__)
fake = Faker()
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///medguard.db"  # uno stesso DB
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
     if not os.path.exists("instance/medguard.db"):
        db.create_all()
        print("Database creato.")
        username1 = "angelo"
        password1 = "barone"
        user = userModels.create_user(app, username1, password1, "S")
        for _ in range(10):
            username = fake.user_name()
            password = fake.password(length=10)
            user = userModels.User(username=username)#, clear_password=password)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
        generator.genera_dataset(20, app)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    type = userModels.validate_user(app, username, password)
    print("L'utente " + username + " ha effettuato il login con auth: " + type)
    if type:
        if type == "S":
            #"http://127.0.0.1:5001/setToken"
            url = "https://medguard-trustedautority.onrender.com/setToken"
            data = {"username": username}
            response = requests.post(url, json=data)
            token = response.json()["token"]
            return jsonify({"success": True, "token": token, "username": username, "type" : type}), 200
        else:
            return jsonify({"success": True, "token": "fake-jwt-token", "username": username, "type" : type}), 200
    else:
        return jsonify({"success": False, "message": "Credenziali errate"}), 401

@app.route('/checkAuthorization', methods=['POST'])
def checkAuthorization():
    data = request.get_json()
    username = data.get("username")
    hash = userModels.check_authorization(app, username)
    return jsonify({"success": True, "hash": hash}), 200

@app.route('/encDataReceiver', methods=['POST'])
def encDataReceiver():
    data = request.get_json()
    username = data.get("clinic")
    enc_data = data.get("data")
    n_str = data.get("n")
    n = int(n_str)
    pubkey = paillier.PaillierPublicKey(n)

    if allData.upload_data(app, username, enc_data):
        homomorphicData.upload_homomorphic_data(app, enc_data, pubkey)
        return jsonify({"success": True}), 200
    else:
        return jsonify({"success": False}), 450

@app.route('/encDataSender', methods=['POST'])
def encDataSender():
    data = homomorphicData.get_homomorphic_data(app)
    return jsonify({"success": True, "data": data}), 200

@app.route('/PublishData', methods=['POST'])
def PublishData():
    data = request.get_json()
    payload = data.get("payload", {})
    if publishedData.upload_data(app, payload):
        return jsonify({"success": True}), 200
    else:
        return jsonify({"success": False}), 450

@app.route('/getPublishedData', methods=['GET'])
def getPublishedData():
    data = publishedData.get_data(app)
    return jsonify({"success": True, "data": data}), 200

if __name__ == "__main__":
    app.run(port=5000)