import json

from faker import Faker
from flask import Flask, request, jsonify
from extensions import db
from userModels import User

fake = Faker()

class AllData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    data = db.Column(db.String(1000), nullable=False)

def upload_data(app, username, encdata):
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if user:
            json_data = json.dumps(encdata)
            data = AllData(username=username, data=json_data)
            db.session.add(data)
            db.session.commit()
            return True
        else:
            return False