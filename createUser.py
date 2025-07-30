import userModels


username = input("Inserisci username: ")
password = input("Inserisci password: ")
type = input("Inserisci tipo (A = hospital, S = authorized, C = admin): ")

userModels.create_user(username, password, type)