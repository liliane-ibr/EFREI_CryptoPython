# __init__.py
from cryptography.fernet import Fernet, InvalidToken
from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')


# --- Gestion clé persistante ---
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
    valeur_bytes = valeur.encode()
    token = f.encrypt(valeur_bytes)
    return f"Valeur encryptée : {token.decode()}"


# --- Route de décryptage ---
@app.route('/decrypt/<string:token>')
def decryptage(token):
    try:
        valeur_bytes = f.decrypt(token.encode())
        valeur = valeur_bytes.decode()
        return f"Valeur déchiffrée : {valeur}"
    except InvalidToken:
        return "Erreur : le token fourni est invalide ou la clé ne correspond pas.", 400
    except Exception as e:
        return f"Erreur interne : {str(e)}", 500


if __name__ == "__main__":
    app.run(debug=True)
