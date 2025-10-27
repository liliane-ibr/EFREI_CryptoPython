from cryptography.fernet import Fernet, InvalidToken
from flask import Flask, render_template, request, current_app
from flask import render_template_string, jsonify
from flask import json
from urllib.request import urlopen
import sqlite3

app = Flask(__name__)

# --- Page d'accueil ---
@app.route('/')
def hello_world():
    return render_template('hello.html')


# --- Clé automatique pour Exercice 1 ---
KEY_FILE = "secret.key"
try:
    with open(KEY_FILE, "rb") as fkey:
        key = fkey.read()
except FileNotFoundError:
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as fkey:
        fkey.write(key)

f = Fernet(key)


# --- Route d'encryptage Exercice 1 ---
@app.route('/encrypt/<string:valeur>')
def encryptage(valeur):
    valeur_bytes = valeur.encode()  # Conversion str -> bytes
    token = f.encrypt(valeur_bytes)  # Encrypt la valeur
    return f"Valeur encryptée : {token.decode()}"  # Retourne le token en str


# --- Route de décryptage Exercice 1 ---
@app.route('/decrypt/<string:token>')
def decryptage(token):
    try:
        valeur_bytes = f.decrypt(token.encode())  # Déchiffre le token
        valeur = valeur_bytes.decode()
        return f"Valeur déchiffrée : {valeur}"
    except InvalidToken:
        return "Erreur : le token fourni est invalide ou la clé ne correspond pas.", 400
    except Exception as e:
        current_app.logger.exception("Erreur de décryptage")
        return f"Erreur interne : {str(e)}", 500


# --- Route d'encryptage avec clé personnelle Exercice 2 ---
@app.route('/encrypt_personal/<string:valeur>')
def encrypt_personal(valeur):
    key_personnelle = request.args.get('key')
    if not key_personnelle:
        return "Erreur : merci de fournir une clé avec ?key=<votre_clé>", 400
    try:
        f_personal = Fernet(key_personnelle.encode())
        token = f_personal.encrypt(valeur.encode())
        return f"Valeur encryptée avec votre clé : {token.decode()}"
    except Exception as e:
        return f"Erreur : clé invalide. Détails : {str(e)}", 400


# --- Route de décryptage avec clé personnelle Exercice 2 ---
@app.route('/decrypt_personal/<string:token>')
def decrypt_personal(token):
    key_personnelle = request.args.get('key')
    if not key_personnelle:
        return "Erreur : merci de fournir une clé avec ?key=<votre_clé>", 400
    try:
        f_personal = Fernet(key_personnelle.encode())
        valeur = f_personal.decrypt(token.encode()).decode()
        return f"Valeur déchiffrée avec votre clé : {valeur}"
    except InvalidToken:
        return "Erreur : token invalide ou clé incorrecte", 400
    except Exception as e:
        return f"Erreur interne : {str(e)}", 500


# --- Lancement de l'application ---
if __name__ == "__main__":
    app.run(debug=True)
