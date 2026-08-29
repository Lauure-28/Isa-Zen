from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from deep_translator import GoogleTranslator
import requests
from datetime import datetime, date
import random
import os
from data import VIDEOS_DATA

# On importe la liste complète des 87 cartes depuis notre nouveau fichier
from oracles import ORACLES_BIEN_ETRE

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cartes.db'

# ⚠️ Clé secrète indispensable pour Flask
app.secret_key = 'Isa-ZEN-23.12'

db = SQLAlchemy(app)

class Carte(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

with app.app_context():
    db.create_all()

def get_horoscope_api():
    try:
        url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily?sign=aries&day=today"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            texte_anglais = response.json()['data']['horoscope']
            try:
                return GoogleTranslator(source='en', target='fr').translate(texte_anglais)
            except Exception:
                # Texte de secours élégant en français si la traduction bloque
                return "Une énergie sereine et lumineuse vous accompagne aujourd'hui, prenez le temps d'accueillir l'instant présent."
        return "Le ciel est calme, profitez de l'instant."
    except Exception as e:
        return "Une énergie sereine vous accompagne aujourd'hui, prenez le temps de respirer."

@app.route('/')
def home():
    now = datetime.now()
    jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    mois = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
    date_fr = f"{jours[now.weekday()]} {now.day} {mois[now.month-1]} {now.year}"
    heure_fr = now.strftime("%H:%M")

    today_ordinal = date.today().toordinal()
    random.seed(today_ordinal)
    
    carte_du_jour = random.choice(ORACLES_BIEN_ETRE)
    
    random.seed()

    horoscope_du_jour = get_horoscope_api()

    return render_template('index.html', 
                           carte=carte_du_jour, 
                           horoscope=horoscope_du_jour, 
                           date=date_fr, 
                           heure=heure_fr,
                           data=VIDEOS_DATA)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
