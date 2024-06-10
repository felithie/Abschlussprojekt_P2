import json

# Funktion zum Laden der Benutzerdatenbank aus einer Datei
def load_user_db(USER_DB_FILE):
    try:
        with open(USER_DB_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Funktion zum Speichern der Benutzerdatenbank in eine Datei
def save_user_db(USER_DB_FILE, users):
    with open(USER_DB_FILE, 'w') as f:
        json.dump(users, f)