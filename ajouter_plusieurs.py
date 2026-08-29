from app import app, db, Carte

# Ajoutez ici autant de cartes que vous voulez !
nouvelles_cartes = [
    {"nom": "La Lune", "message": "Faites confiance à votre intuition aujourd'hui."},
    {"nom": "Le Monde", "message": "Une étape se termine, une belle réussite approche."},
    {"nom": "L'Ermite", "message": "Prenez un moment pour vous, le silence est votre allié."},
    {"nom": "La Papesse", "message": "La patience est la clé de votre épanouissement."},
    {"nom": "Le Pendu", "message": "Lâcher prise ne signifie pas abandonner, mais accepter."},
]

def ajouter_en_masse():
    with app.app_context():
        for c in nouvelles_cartes:
            carte = Carte(nom=c['nom'], message=c['message'])
            db.session.add(carte)
        db.session.commit()
        print(f"{len(nouvelles_cartes)} cartes ont été ajoutées avec succès !")

if __name__ == "__main__":
    ajouter_en_masse()