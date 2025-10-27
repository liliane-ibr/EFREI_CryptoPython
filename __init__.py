import os
from cryptography.fernet import Fernet

# --- Clé persistante ---
KEY_FILE = "secret.key"

if os.path.exists(KEY_FILE):
    key = open(KEY_FILE, "rb").read()
else:
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as fkey:
        fkey.write(key)

f = Fernet(key)
