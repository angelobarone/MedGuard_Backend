import random

import requests
from phe import paillier
from app import app
import homomorphicData

macroarea = ["Nord", "Centro", "Sud"]

malattie = ["Diabete", "Ipertensione", "Asma", "Influenza", "Covid-19"]

#mesi = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]
url = "http://127.0.0.1:5001/getPublicKey"
data = {"username": "admin"}

response = requests.post(url, json=data)

if response.status_code == 200:
    response_json = response.json()
    n = int(response_json["n"])
    pubkey = paillier.PaillierPublicKey(n)
    print("Chiave pubblica caricata correttamente! " + str(pubkey))
else:
    print("Errore durante il caricamento della chiave pubblica!")
    exit(1)


# Funzione per generare un record casuale
def genera_record():
    # Genera valori casuali
    eta_val = random.randint(1, 100)
    colesterolo_val = random.randint(120, 280)
    pressione_val = random.randint(90, 200)
    glicemia_val = random.randint(70, 200)
    fumatore_val = random.randint(0, 1)
    febbre_val = random.randint(0, 1)
    tosse_val = random.randint(0, 1)
    difficolta_val = random.randint(0, 1)
    stanchezza_val = random.randint(0, 1)
    genere_val = random.randint(0, 1)
    peso_val = random.randint(50, 150)
    altezza_val = random.randint(150, 220)
    enc_data =  {
        "macroarea": random.choice(macroarea),
        "malattia": random.choice(malattie),
        #"mese": random.choice(mesi),
        #"anno": random.randint(2020, 2025),
        # Campi di somma (richiesti dal DB)
        "count_sum": hex(pubkey.encrypt(1).ciphertext()),  # Ogni record conta come 1 paziente
        "eta_sum": hex(pubkey.encrypt(eta_val).ciphertext()),  # Somma iniziale = valore singolo
        "colesterolo_sum": hex(pubkey.encrypt(colesterolo_val).ciphertext()),
        "pressione_sum": hex(pubkey.encrypt(pressione_val).ciphertext()),
        "glucosio_sum": hex(pubkey.encrypt(glicemia_val).ciphertext()),
        "fumatore_sum": hex(pubkey.encrypt(fumatore_val).ciphertext()),
        "febbre_sum": hex(pubkey.encrypt(febbre_val).ciphertext()),
        "tosse_sum": hex(pubkey.encrypt(tosse_val).ciphertext()),
        "difficolta_sum": hex(pubkey.encrypt(difficolta_val).ciphertext()),
        "stanchezza_sum": hex(pubkey.encrypt(stanchezza_val).ciphertext()),
        # Se richiesti dal DB, aggiungi anche questi con valori default
        "genere_sum": hex(pubkey.encrypt(genere_val).ciphertext()),  # Sostituisci con valore appropriato
        "peso_sum": hex(pubkey.encrypt(peso_val).ciphertext()),    # Sostituisci con valore appropriato
        "altezza_sum": hex(pubkey.encrypt(altezza_val).ciphertext())   # Sostituisci con valore appropriato
    }
    return enc_data

# Funzione per generare un dataset
def genera_dataset(n):
    for i in range(n):
        print("Generazione record " + str(i+1) + " di " + str(n))
        record = genera_record()
        homomorphicData.upload_homomorphic_data(app, record, pubkey)

# Esempio: genera 50 record e salvali in CSV
if __name__ == "__main__":
    genera_dataset(50)

