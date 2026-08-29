from flask import Flask, render_template, request, redirect, url_for, session
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

# ⚠️ Mets ici une clé secrète aléatoire
app.secret_key = 'Isa-ZEN-23.12'

# 👉 Mets ici ton mot de passe secret pour te connecter
MOT_DE_PASSE_SECRET = "Isagil01"

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
        response = requests.get(url)
        if response.status_code == 200:
            texte_anglais = response.json()['data']['horoscope']
            return GoogleTranslator(source='en', target='fr').translate(texte_anglais)
        return "Le ciel est calme, profitez de l'instant."
    except Exception as e:
        return f"Erreur technique : {str(e)}"

@app.route('/login', methods=['GET', 'POST'])
def login():
    erreur = None
    if request.method == 'POST':
        if request.form.get('password') == MOT_DE_PASSE_SECRET:
            session['connecte'] = True
            return redirect(url_for('home'))
        else:
            erreur = "Mot de passe incorrect."
    
    return '''
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Connexion - Espace Zen</title>
        <style>
            body { background-color: #faf8f5; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .login-box { background: white; padding: 30px; border-radius: 10px; border: 2px solid #e8decb; text-align: center; width: 300px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
            .input-group { position: relative; width: 100%; margin: 15px 0; }
            input { width: 100%; padding: 10px 40px 10px 10px; border: 1px solid #ccc; border-radius: 5px; box-sizing: border-box; font-size: 16px; }
            .toggle-btn { position: absolute; right: 10px; top: 50%; transform: translateY(-50%); background: none; border: none; cursor: pointer; font-size: 1.1em; padding: 0; width: auto; color: #666; }
            button[type="submit"] { background: #b38f4d; color: white; border: none; padding: 10px; width: 100%; border-radius: 5px; cursor: pointer; font-weight: bold; font-size: 16px; }
            button[type="submit"]:hover { background: #9a783d; }
            .error { color: #d9534f; font-size: 0.9em; margin-bottom: 10px; }
        </style>
    </head>
    <body>
        <div class="login-box">
            <h2>🔒 Espace Privé</h2>
            {% if erreur %}<p class="error">{{ erreur }}</p>{% endif %}
            <form method="POST">
                <div class="input-group">
                    <input type="password" id="password" name="password" placeholder="Mot de passe" required autofocus autocomplete="current-password">
                    <button type="button" class="toggle-btn" onclick="togglePassword()">👁️</button>
                </div>
                <button type="submit">Entrer</button>
            </form>
        </div>

        <script>
            function togglePassword() {
                const input = document.getElementById('password');
                if (input.type === 'password') {
                    input.type = 'text';
                } else {
                    input.type = 'password';
                }
            }
        </script>
    </body>
    </html>
    '''

@app.route('/logout')
def logout():
    session.pop('connecte', None)
    return redirect(url_for('login'))

@app.route('/')
def home():
    if not session.get('connecte'):
        return redirect(url_for('login'))

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