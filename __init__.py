# __init__.py
import os
from flask import Flask, render_template, current_app
from cryptography.fernet import Fernet, InvalidToken

app = Flask(__name__)

# --- Page d'accueil ---
@app.route('/')
def home():
    return render_template('hello.html')


# --- Clé persistante ---
KEY_FILE = "secret.key"

if os.path.exists(KEY_FILE):
    key = open(KEY_FILE, "rb").read()
else:
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as fkey:
        fkey.write(key)

f = Fernet(key)


# --- Route d'encryptage ---
@app.route('/encrypt/<string:valeur>')
def encryptage(valeur):
    valeur_bytes = valeur.encode()  # Conversion str -> bytes
    token = f.encrypt(valeur_bytes)  # Encrypt la valeur
    return f"Valeur encryptée : {token.decode()}"  # Retourne le token en str


# --- Route de décryptage ---
@app.route('/decrypt/<string:token>')
def decryptage(token):
    try:
        valeur_bytes = f.decrypt(token.encode())  # Déchiffre le token
        valeur = valeur_bytes.decode()            # Conversion bytes -> str
        return f"Valeur déchiffrée : {valeur}"
    except InvalidToken:
        return "Erreur : le token fourni est invalide ou la clé ne correspond pas.", 400
    except Exception as e:
        current_app.logger.exception("Erreur de décryptage")
        return f"Erreur interne : {str(e)}", 500


# --- Lancement de l'application ---
if __name__ == "__main__":
    app.run(debug=True)
