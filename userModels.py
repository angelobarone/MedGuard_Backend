import os
from faker import Faker
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import requests
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # database SQLite in un file locale
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
fake = Faker()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    clear_password = db.Column(db.String(150), nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(1), nullable=False, default="A")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


def initialize_database():
    for _ in range(10):
        username = fake.user_name()
        password = fake.password(length=10)
        user = User(username=username, clear_password=password)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

def check_database():
    with app.app_context():
        if not os.path.exists("instance/users.db"):
            db.create_all()
            initialize_database()

def validate_user(username, password):
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user.type
        else:
            return False

def check_authorization(username):
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if user.type == "S":
            return user.password_hash
        else:
            return False

def create_user(username, password, type):
    with app.app_context():
        existing = User.query.filter_by(username=username).first()
        if existing:
            print(f"Utente '{username}' esiste già.")
            return

        user = User(username=username, clear_password=password, type=type)
        user.set_password(password)
        if type == "S":
            url = "http://127.0.0.1:5001/addAuthUser"
            data = {"username": username, "password": user.password_hash}
            requests.post(url, json=data)
        db.session.add(user)
        db.session.commit()
