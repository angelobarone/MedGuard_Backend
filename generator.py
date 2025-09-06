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

import requests
import time
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_server_health(url, timeout=10):
    """Controlla se il server è raggiungibile"""
    try:
        response = requests.get(url.replace("getPublicKey", ""), timeout=timeout)
        return response.status_code == 200
    except:
        return False


def genera_dataset(n, app, max_retries=5, initial_delay=5):
    base_url = "https://medguard-trustedautority.onrender.com"
    url = f"{base_url}/getPublicKey"
    data = {"username": "admin"}

    logger.info("Controllo dello stato del server...")

    # Prima verifica se il server è raggiungibile
    if not check_server_health(base_url):
        logger.warning("Il server non sembra raggiungibile. Attendere l'avvio...")
        time.sleep(initial_delay)

    for attempt in range(max_retries):
        try:
            logger.info(f"Tentativo {attempt + 1} di {max_retries} - {datetime.now()}")

            # Aumenta il timeout progressivamente
            current_timeout = 30 + (attempt * 10)
            response = requests.post(url, json=data, timeout=current_timeout)

            logger.info(f"Status code ricevuto: {response.status_code}")

            if response.status_code == 200:
                response_json = response.json()
                n_value = int(response_json["n"])
                pubkey = paillier.PaillierPublicKey(n_value)
                logger.info("Chiave pubblica ottenuta con successo!")
                break

            elif response.status_code == 502:
                logger.warning("Server non pronto (502 Bad Gateway). Il servizio potrebbe essere in avvio...")
                if attempt < max_retries - 1:
                    wait_time = initial_delay * (2 ** attempt)  # Backoff esponenziale
                    logger.info(f"Attesa di {wait_time} secondi prima del prossimo tentativo...")
                    time.sleep(wait_time)
                    continue

            else:
                logger.error(f"Errore HTTP inaspettato: {response.status_code}")
                logger.error(f"Response text: {response.text}")

        except requests.Timeout:
            logger.warning(f"Timeout dopo {current_timeout} secondi")
            if attempt < max_retries - 1:
                wait_time = initial_delay * (2 ** attempt)
                logger.info(f"Attesa di {wait_time} secondi...")
                time.sleep(wait_time)

        except requests.ConnectionError:
            logger.warning("Errore di connessione - server potrebbe non essere attivo")
            if attempt < max_retries - 1:
                wait_time = initial_delay * (2 ** attempt)
                logger.info(f"Attesa di {wait_time} secondi...")
                time.sleep(wait_time)

        except Exception as e:
            logger.error(f"Errore imprevisto: {e}")
            if attempt < max_retries - 1:
                time.sleep(initial_delay * (attempt + 1))

    else:
        logger.error("Impossibile connettersi al server dopo tutti i tentativi")
        return False

    # Se siamo qui, abbiamo la chiave pubblica - procedi con la generazione
    logger.info("Inizio generazione dataset...")
    successful_uploads = 0

    for i in range(n):
        try:
            logger.info(f"Generazione record {i + 1} di {n}")
            record = genera_record(pubkey)
            homomorphicData.upload_homomorphic_data(app, record, pubkey)
            successful_uploads += 1
            time.sleep(0.5)  # Pausa tra le richieste

        except Exception as e:
            logger.error(f"Errore nel record {i + 1}: {e}")
            continue

    logger.info(f"Processo completato. Upload riusciti: {successful_uploads}/{n}")
    return True

# Esempio: genera 50 record e salvali in CSV
#if __name__ == "__main__":
    #genera_dataset(100, app.app)

