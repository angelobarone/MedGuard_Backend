import userModels
from app import app

username = input("Inserisci username: ")
password = input("Inserisci password: ")
type = input("Inserisci tipo (A = hospital, S = authorized: ")

userModels.create_user(app, username, password, type)