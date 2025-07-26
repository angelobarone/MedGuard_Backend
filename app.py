from flask import Flask, request, jsonify
from flask_cors import CORS
import models
app = Flask(__name__)
CORS(app)  # permette le richieste dal frontend React
models.check_database()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    type = models.validate_user(username, password)
    print("L'utente " + username + "ha effettuato il login con auth: " + type)
    if type:
        return jsonify({"success": True, "token": "fake-jwt-token", "username": username, "publicKey": "fake-public-key", "type" : type}), 200
    else:
        return jsonify({"success": False, "message": "Credenziali errate"}), 401