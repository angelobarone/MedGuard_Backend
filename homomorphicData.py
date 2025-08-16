from phe import paillier
import base64
import json
from extensions import db

class Aggregati(db.Model):
    provincia = db.Column(db.String, primary_key=True)
    malattia = db.Column(db.String, primary_key=True)
    mese = db.Column(db.String, primary_key=True)
    anno = db.Column(db.String, primary_key=True)

    count_sum = db.Column(db.Text, nullable=False)
    eta_sum = db.Column(db.Text, nullable=False)
    colesterolo_sum = db.Column(db.Text, nullable=False)
    pressione_sum = db.Column(db.Text, nullable=False)
    glucosio_sum = db.Column(db.Text, nullable=False)

    fumatore_sum = db.Column(db.Text, nullable=False)
    febbre_sum = db.Column(db.Text, nullable=False)
    tosse_sum = db.Column(db.Text, nullable=False)
    difficolta_sum = db.Column(db.Text, nullable=False)
    stanchezza_sum = db.Column(db.Text, nullable=False)
    genere_sum = db.Column(db.Text, nullable=False)
    peso_sum = db.Column(db.Text, nullable=False)
    altezza_sum = db.Column(db.Text, nullable=False)

def hex_to_int(hex_str:str) -> int:
    return int(hex_str, 16)

def int_to_hex(c:int) -> str:
    return hex(c)

def homomorhic_sum(c1, c2, public_key):
    i1 = hex_to_int(c1)
    i2 = hex_to_int(c2)

    n_sq = public_key.n ** 2
    somma = (i1 * i2) % n_sq
    return int_to_hex(somma)


def upload_homomorphic_data(app, enc_data, public_key):
    with app.app_context():
        provincia = enc_data.get("provincia")
        malattia = enc_data.get("malattia")
        mese = enc_data.get("mese")
        anno = enc_data.get("anno")

        row = Aggregati.query.filter_by(provincia=provincia, malattia=malattia, mese=mese, anno=anno).first()

        if not row:
            row = Aggregati(
                provincia=provincia,
                malattia=malattia,
                mese=mese,
                anno=anno,
                count_sum=enc_data.get("count_sum"),
                eta_sum=enc_data.get("eta_sum"),
                colesterolo_sum=enc_data.get("colesterolo_sum"),
                pressione_sum=enc_data.get("pressione_sum"),
                glucosio_sum=enc_data.get("glucosio_sum"),
                fumatore_sum=enc_data.get("fumatore_sum"),
                febbre_sum=enc_data.get("febbre_sum"),
                tosse_sum=enc_data.get("tosse_sum"),
                difficolta_sum=enc_data.get("difficolta_sum"),
                stanchezza_sum=enc_data.get("stanchezza_sum"),
                genere_sum=enc_data.get("genere_sum"),
                peso_sum=enc_data.get("peso_sum"),
                altezza_sum=enc_data.get("altezza_sum")
            )
            db.session.add(row)

        else:
            for field in [
                "count_sum", "eta_sum", "colesterolo_sum", "pressione_sum", "glucosio_sum",
                "fumatore_sum", "febbre_sum", "tosse_sum", "difficolta_sum", "stanchezza_sum", "genere_sum", "peso_sum", "altezza_sum"
            ]:
                setattr(row, field, homomorhic_sum(getattr(row, field), enc_data[field], public_key))

        db.session.commit()
        return True

def get_homomorphic_data(app):
    with app.app_context():
        out = []
        for row in Aggregati.query.all():
            out.append({
                "provincia": row.provincia,
                "malattia": row.malattia,
                "mese": row.mese,
                "anno": row.anno,
                "count_sum": row.count_sum,
                "eta_sum": row.eta_sum,
                "colesterolo_sum":row.colesterolo_sum,
                "pressione_sum": row.pressione_sum,
                "glucosio_sum": row.glucosio_sum,
                "fumatore_sum": row.fumatore_sum,
                "febbre_sum": row.febbre_sum,
                "tosse_sum": row.tosse_sum,
                "difficolta_sum": row.difficolta_sum,
                "stanchezza_sum": row.stanchezza_sum,
                "genere_sum": row.genere_sum,
                "peso_sum": row.peso_sum,
                "altezza_sum": row.altezza_sum
            })
        return out
