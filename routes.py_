# routes.py
# Déclare une fonction init_routes(app) pour s'intégrer facilement dans create_app/__init__.py

from flask import request, jsonify, current_app
from cryptography.fernet import Fernet, InvalidToken
import hashlib, base64

def key_from_password(password: str) -> bytes:
    """
    Si l'utilisateur fournit un mot de passe simple,
    on dérive une clé Fernet valide (base64 urlsafe, 32 bytes) via SHA-256.
    """
    h = hashlib.sha256(password.encode('utf-8')).digest()   # 32 bytes
    return base64.urlsafe_b64encode(h)

def decrypt_token_with_key(token: str, key: str) -> str:
    """
    Décrypte un token (chaîne) avec une clé (soit clé Fernet base64, soit mot de passe).
    Retourne le texte déchiffré en str ou lève une exception.
    """
    # Déterminer si la clé semble déjà être une clé Fernet (base64 urlsafe -> longueur ≈ 44)
    try:
        key_bytes = key.encode('utf-8')
        # tentative rapide : si base64-correct, on l'utilise ; sinon on dérive depuis mot de passe
        # On essaye de construire Fernet, si ça échoue on dérive depuis password.
        f = Fernet(key_bytes)
    except Exception:
        # dériver depuis password
        key_bytes = key_from_password(key)
        f = Fernet(key_bytes)

    # Déchiffrage
    decrypted_bytes = f.decrypt(token.encode('utf-8'))
    return decrypted_bytes.decode('utf-8')

def init_routes(app):
    @app.route('/decrypt/', methods=['POST'])
    def decrypt_route():
        """
        Endpoint POST /decrypt/
        Attendu JSON:
        {
          "token": "<texte chiffré (Fernet)>",
          "key": "<clé Fernet base64 OU mot de passe simple>"
        }
        Réponse JSON:
        { "decrypted": "<texte en clair>" }
        """
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "JSON attendu (token + key)"}), 400

        token = data.get('token')
        key = data.get('key')
        if not token or not key:
            return jsonify({"error": "Vous devez fournir 'token' et 'key'"}), 400

        try:
            decrypted = decrypt_token_with_key(token, key)
            return jsonify({"decrypted": decrypted}), 200
        except InvalidToken:
            return jsonify({"error": "Token ou clé invalide (InvalidToken)"}), 400
        except Exception as e:
            current_app.logger.exception("Erreur de décryptage")
            return jsonify({"error": str(e)}), 500
