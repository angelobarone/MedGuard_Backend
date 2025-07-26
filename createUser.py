import models


username = input("Inserisci username: ")
password = input("Inserisci password: ")
type = input("Inserisci tipo (A = hospital, S = authorized, C = admin): ")

models.create_user(username, password, type)