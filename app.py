from flask import Flask, request, jsonify
from flask_cors import CORS
import userModels
app = Flask(__name__)
CORS(app)  # permette le richieste dal frontend React
userModels.check_database()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    type = userModels.validate_user(username, password)
    print("L'utente " + username + "ha effettuato il login con auth: " + type)
    if type:
        return jsonify({"success": True, "token": "fake-jwt-token", "username": username, "type" : type}), 200
    else:
        return jsonify({"success": False, "message": "Credenziali errate"}), 401

@app.route('/checkAuthorization', methods=['POST'])
def checkAuthorization():
    data = request.get_json()
    username = data.get("username")
    return userModels.check_authorization(username)

@app.route('/uploadData', methods=['POST']){

}

@app.route('/downloadData', methods=['POST']){

}