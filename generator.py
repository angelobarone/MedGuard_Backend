import random

import requests
from phe import paillier
import homomorphicData

macroarea = ["Nord", "Centro", "Sud"]
malattie = ["Diabete", "Ipertensione", "Asma", "Influenza", "Covid-19", "Bronchite", "Artrosi", "Gastrite",
                "Osteoporosi", "Dermatite"]


# Funzione per generare un record casuale
def genera_record(pubkey):
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
        "count_sum": hex(pubkey.encrypt(1).ciphertext()),
        "eta_sum": hex(pubkey.encrypt(eta_val).ciphertext()),
        "colesterolo_sum": hex(pubkey.encrypt(colesterolo_val).ciphertext()),
        "pressione_sum": hex(pubkey.encrypt(pressione_val).ciphertext()),
        "glucosio_sum": hex(pubkey.encrypt(glicemia_val).ciphertext()),
        "fumatore_sum": hex(pubkey.encrypt(fumatore_val).ciphertext()),
        "febbre_sum": hex(pubkey.encrypt(febbre_val).ciphertext()),
        "tosse_sum": hex(pubkey.encrypt(tosse_val).ciphertext()),
        "difficolta_sum": hex(pubkey.encrypt(difficolta_val).ciphertext()),
        "stanchezza_sum": hex(pubkey.encrypt(stanchezza_val).ciphertext()),
        "genere_sum": hex(pubkey.encrypt(genere_val).ciphertext()),
        "peso_sum": hex(pubkey.encrypt(peso_val).ciphertext()),
        "altezza_sum": hex(pubkey.encrypt(altezza_val).ciphertext())
    }
    return enc_data

# Funzione per generare un dataset
import requests
import time
from requests.exceptions import RequestException, Timeout


def genera_dataset(n, app, max_retries=3, timeout=30):
    url = "https://medguard-trustedautority.onrender.com/getPublicKey"
    data = {"username": "admin"}

    # Tentativi per ottenere la chiave pubblica
    for attempt in range(max_retries):
        try:
            print(f"Tentativo {attempt + 1} di connessione al server...")
            response = requests.post(url, json=data, timeout=timeout)

            if response.status_code == 200:
                response_json = response.json()
                n = int(response_json["n"])
                pubkey = paillier.PaillierPublicKey(n)
                print("Chiave pubblica caricata correttamente! " + str(pubkey))
                break
            else:
                print(f"Status code: {response.status_code}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Backoff esponenziale

        except Timeout:
            print(f"Timeout nel tentativo {attempt + 1}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
        except RequestException as e:
            print(f"Errore di connessione: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
        except Exception as e:
            print(f"Errore imprevisto: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
    else:
        print("Errore: impossibile connettersi al server dopo tutti i tentativi")
        exit(1)

    # Generazione dei record
    for i in range(n):
        print("Generazione record " + str(i + 1) + " di " + str(n))
        record = genera_record(pubkey)

        # Anche per l'upload aggiungi ritardi e gestione errori
        try:
            homomorphicData.upload_homomorphic_data(app, record, pubkey)
            time.sleep(1)  # Piccola pausa tra le richieste
        except Exception as e:
            print(f"Errore durante l'upload del record {i + 1}: {e}")
            # Decide se continuare o fermarsi
            continue

# Esempio: genera 50 record e salvali in CSV
#if __name__ == "__main__":
    #genera_dataset(100, app.app)

