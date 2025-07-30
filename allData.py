import os

from faker import Faker
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

import userModels
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///allData.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
fake = Faker()

class AllData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    data = db.Column(db.String(500), nullable=False)

def check_database():
    with app.app_context():
        if not os.path.exists("instance/allData.db"):
            db.create_all()

def upload_data(username, data):
    with app.app_context():
        user = userModels.User.query.filter_by(username=username).first()
        if user:
            data = AllData(username=username, data=data)
            db.session.add(data)
            db.session.commit()
            return True
        else:
            return False