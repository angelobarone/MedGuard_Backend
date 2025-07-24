import models


username = input("Inserisci username: ")
password = input("Inserisci password: ")
type = input("Inserisci tipo (A = client, B = stat, C = admin): ")

models.create_user(username, password, type)