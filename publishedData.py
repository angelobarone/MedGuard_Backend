from extensions import db

class PublishedData(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    n_pazienti = db.Column(db.Integer, nullable=False)
    eta_media = db.Column(db.Float, nullable=False)
    glicemia_media = db.Column(db.Float, nullable=False)
    colesterolo_media = db.Column(db.Float, nullable=False)
    prevalenza_diabete = db.Column(db.Float, nullable=False)
    percentuale_fumatori = db.Column(db.Float, nullable=False)
    percentuale_uomini = db.Column(db.Float, nullable=False)
    percentuale_femmine = db.Column(db.Float, nullable=False)

    n_nord = db.Column(db.Integer, nullable=False)
    eta_media_nord = db.Column(db.Float, nullable=False)
    glicemia_media_nord = db.Column(db.Float, nullable=False)
    colesterolo_media_nord = db.Column(db.Float, nullable=False)
    prevalenza_diabete_nord = db.Column(db.Float, nullable=False)
    percentuale_fumatori_nord = db.Column(db.Float, nullable=False)
    percentuale_uomini_nord = db.Column(db.Float, nullable=False)
    percentuale_femmine_nord = db.Column(db.Float, nullable=False)

    n_sud = db.Column(db.Integer, nullable=False)
    eta_media_sud = db.Column(db.Float, nullable=False)
    glicemia_media_sud = db.Column(db.Float, nullable=False)
    colesterolo_media_sud = db.Column(db.Float, nullable=False)
    prevalenza_diabete_sud = db.Column(db.Float, nullable=False)
    percentuale_fumatori_sud = db.Column(db.Float, nullable=False)
    percentuale_uomini_sud = db.Column(db.Float, nullable=False)
    percentuale_femmine_sud = db.Column(db.Float, nullable=False)

    n_centro = db.Column(db.Integer, nullable=False)
    eta_media_centro = db.Column(db.Float, nullable=False)
    glicemia_media_centro = db.Column(db.Float, nullable=False)
    colesterolo_media_centro = db.Column(db.Float, nullable=False)
    prevalenza_diabete_centro = db.Column(db.Float, nullable=False)
    percentuale_fumatori_centro = db.Column(db.Float, nullable=False)
    percentuale_uomini_centro = db.Column(db.Float, nullable=False)
    percentuale_femmine_centro = db.Column(db.Float, nullable=False)

def create_row(data):
    row = PublishedData(
        n_pazienti=data.get("n_pazienti"),
        eta_media=data.get("eta_media"),
        glicemia_media=data.get("glicemia_media"),
        colesterolo_media=data.get("colesterolo_media"),
        prevalenza_diabete=data.get("prevalenza_diabete"),
        percentuale_fumatori=data.get("percentuale_fumatori"),
        percentuale_uomini=data.get("percentuale_uomini"),
        percentuale_femmine=data.get("percentuale_donne"),
        n_nord=data.get("n_nord"),
        eta_media_nord=data.get("eta_media_nord"),
        glicemia_media_nord=data.get("glicemia_media_nord"),
        colesterolo_media_nord=data.get("colesterolo_media_nord"),
        prevalenza_diabete_nord=data.get("prevalenza_diabete_nord"),
        percentuale_fumatori_nord=data.get("percentuale_fumatori_nord"),
        percentuale_uomini_nord=data.get("percentuale_uomini_nord"),
        percentuale_femmine_nord=data.get("percentuale_donne_nord"),
        n_sud=data.get("n_sud"),
        eta_media_sud=data.get("eta_media_sud"),
        glicemia_media_sud=data.get("glicemia_media_sud"),
        colesterolo_media_sud=data.get("colesterolo_media_sud"),
        prevalenza_diabete_sud=data.get("prevalenza_diabete_sud"),
        percentuale_fumatori_sud=data.get("percentuale_fumatori_sud"),
        percentuale_uomini_sud=data.get("percentuale_uomini_sud"),
        percentuale_femmine_sud=data.get("percentuale_donne_sud"),
        n_centro=data.get("n_centro"),
        eta_media_centro=data.get("eta_media_centro"),
        glicemia_media_centro=data.get("glicemia_media_centro"),
        colesterolo_media_centro=data.get("colesterolo_media_centro"),
        prevalenza_diabete_centro=data.get("prevalenza_diabete_centro"),
        percentuale_fumatori_centro=data.get("percentuale_fumatori_centro"),
        percentuale_uomini_centro=data.get("percentuale_uomini_centro"),
        percentuale_femmine_centro=data.get("percentuale_donne_centro")
    )
    return row

def upload_data(app, data):
    with app.app_context():
        row = PublishedData.query.first()
        if not row:
            row = create_row(data)
            db.session.add(row)

        else:
            db.session.delete(row)
            row = create_row(data)
            db.session.add(row)

        db.session.commit()
        return True

def get_data(app):
    with app.app_context():
        out = []
        for row in PublishedData.query.all():
            out.append({
                "n_pazienti": row.n_pazienti,
                "eta_media": row.eta_media,
                "glicemia_media": row.glicemia_media,
                "colesterolo_media": row.colesterolo_media,
                "prevalenza_diabete": row.prevalenza_diabete,
                "percentuale_fumatori": row.percentuale_fumatori,
                "percentuale_uomini": row.percentuale_uomini,
                "percentuale_donne": row.percentuale_femmine,
                "n_nord": row.n_nord,
                "eta_media_nord": row.eta_media_nord,
                "glicemia_media_nord": row.glicemia_media_nord,
                "colesterolo_media_nord": row.colesterolo_media_nord,
                "prevalenza_diabete_nord": row.prevalenza_diabete_nord,
                "percentuale_fumatori_nord": row.percentuale_fumatori_nord,
                "percentuale_uomini_nord": row.percentuale_uomini_nord,
                "percentuale_donne_nord": row.percentuale_femmine_nord,
                "n_sud": row.n_sud,
                "eta_media_sud": row.eta_media_sud,
                "glicemia_media_sud": row.glicemia_media_sud,
                "colesterolo_media_sud": row.colesterolo_media_sud,
                "prevalenza_diabete_sud": row.prevalenza_diabete_sud,
                "percentuale_fumatori_sud": row.percentuale_fumatori_sud,
                "percentuale_uomini_sud": row.percentuale_uomini_sud,
                "percentuale_donne_sud": row.percentuale_femmine_sud,
                "n_centro": row.n_centro,
                "eta_media_centro": row.eta_media_centro,
                "glicemia_media_centro": row.glicemia_media_centro,
                "colesterolo_media_centro": row.colesterolo_media_centro,
                "prevalenza_diabete_centro": row.prevalenza_diabete_centro,
                "percentuale_fumatori_centro": row.percentuale_fumatori_centro,
                "percentuale_uomini_centro": row.percentuale_uomini_centro,
                "percentuale_donne_centro": row.percentuale_femmine_centro
            })
        return out
