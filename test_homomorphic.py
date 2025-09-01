import pytest
from flask import Flask
from phe import paillier, EncryptedNumber

from extensions import db
from homomorphicData import (
    Aggregati,
    upload_homomorphic_data,
    get_homomorphic_data,
    homomorhic_sum,
    hex_to_int
)

#AMBIENTE DI TEST
@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture
def paillier_keys():
    public_key, private_key = paillier.generate_paillier_keypair()
    return public_key, private_key


# HELPER FUNCTIONS
def encrypt_to_hex(pk, value: int) -> str:
    return format(pk.encrypt(value).ciphertext(), 'x')

def decrypt_from_hex(pk, sk, hex_val: str) -> int:
    return sk.decrypt(EncryptedNumber(pk, hex_to_int(hex_val)))


# TEST SULLA FUNZIONE BASE DI SOMMA
def test_homomorphic_sum(paillier_keys):
    public_key, private_key = paillier_keys

    a, b = 5, 7
    c1 = encrypt_to_hex(public_key, a)
    c2 = encrypt_to_hex(public_key, b)

    c_sum = homomorhic_sum(c1, c2, public_key)

    decrypted = decrypt_from_hex(public_key, private_key, c_sum)
    assert decrypted == a + b


# TEST SUL FLUSSO COMPLETO
def test_upload_and_aggregate(app, paillier_keys):
    public_key, private_key = paillier_keys

    # Primo inserimento
    enc_data1 = {
        "macroarea": "A",
        "malattia": "X",
        "count_sum": encrypt_to_hex(public_key, 1),
        "eta_sum": encrypt_to_hex(public_key, 30),
        "colesterolo_sum": encrypt_to_hex(public_key, 200),
        "pressione_sum": encrypt_to_hex(public_key, 120),
        "glucosio_sum": encrypt_to_hex(public_key, 90),
        "fumatore_sum": encrypt_to_hex(public_key, 1),
        "febbre_sum": encrypt_to_hex(public_key, 0),
        "tosse_sum": encrypt_to_hex(public_key, 0),
        "difficolta_sum": encrypt_to_hex(public_key, 0),
        "stanchezza_sum": encrypt_to_hex(public_key, 0),
        "genere_sum": encrypt_to_hex(public_key, 1),
        "peso_sum": encrypt_to_hex(public_key, 70),
        "altezza_sum": encrypt_to_hex(public_key, 175),
    }
    upload_homomorphic_data(app, enc_data1, public_key)
    # Secondo inserimento con valori diversi
    enc_data2 = {
        **enc_data1,
        "count_sum": encrypt_to_hex(public_key, 1),
        "eta_sum": encrypt_to_hex(public_key, 40),
    }
    upload_homomorphic_data(app, enc_data2, public_key)
    # Recupero dati
    results = get_homomorphic_data(app)
    assert len(results) == 1  # deve esserci una sola riga
    row = results[0]
    # Validazioni con decifratura
    assert decrypt_from_hex(public_key, private_key, row["count_sum"]) == 2
    assert decrypt_from_hex(public_key, private_key, row["eta_sum"]) == 30 + 40
    assert decrypt_from_hex(public_key, private_key, row["colesterolo_sum"]) == 200 + 200
    assert decrypt_from_hex(public_key, private_key, row["peso_sum"]) == 70 + 70