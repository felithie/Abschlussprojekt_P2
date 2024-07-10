import sqlite3

def create_connection():
    conn = sqlite3.connect('data.db')
    return conn
# Die Funktion create_connection() stellt eine Verbindung zur SQLite-Datenbank her und gibt diese zurück.
def init_db():
    conn = create_connection()
    c = conn.cursor()
    # Check if 'users' table exists, create if not
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            email TEXT,
            name TEXT,
            age INTEGER,
            weight REAL,
            height REAL,
            profile_image BLOB,
            firstname TEXT,
            lastname TEXT,
            birth_year INTEGER,
            gender TEXT
        )
    ''')
    # Die Funktion init_db() initialisiert die Datenbank, indem sie die Tabellen 'users' und 'user_files' erstellt, falls sie noch nicht existieren.
    # Die Tabelle 'users' enthält die Benutzerdaten, während die Tabelle 'user_files' die Dateipfade der Benutzerdateien speichert.
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            file_path TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()

def get_user_id(username):
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
        SELECT id FROM users WHERE username = ?
    ''', (username,))
    user_id = c.fetchone()
    conn.close()
    if user_id:
        return user_id[0]
    return None
# Die Funktion get_user_id(username) gibt die Benutzer-ID für einen bestimmten Benutzernamen zurück.

def register_user(username, password, email, name):
    try:
        conn = create_connection()
        c = conn.cursor()
        c.execute('''
            INSERT INTO users (username, password, email, name)
            VALUES (?, ?, ?, ?)
        ''', (username, password, email, name))
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError("Username already exists")
    finally:
        conn.close()
# Die Funktion register_user(username, password, email, name) registriert einen neuen Benutzer in der Datenbank.
# Sie fügt den Benutzernamen, das Passwort, die E-Mail-Adresse und den Namen des Benutzers in die Tabelle 'users' ein.
def get_user(username):
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
        SELECT * FROM users WHERE username = ?
    ''', (username,))
    user = c.fetchone()
    conn.close()
    return user
# Die Funktion get_user(username) gibt die Benutzerdaten für einen bestimmten Benutzernamen zurück.
# Sie sucht in der Tabelle 'users' nach dem Benutzernamen und gibt die entsprechenden Daten zurück.

def update_user(username, age, weight, height, profile_image=None, firstname=None, lastname=None, birth_year=None, gender=None):
    try:
        conn = create_connection()
        c = conn.cursor()
        if profile_image:
            c.execute('''
                UPDATE users
                SET age = ?, weight = ?, height = ?, profile_image = ?, firstname = ?, lastname = ?, birth_year = ?, gender = ?
                WHERE username = ?
            ''', (age, weight, height, profile_image, firstname, lastname, birth_year, gender, username))
        else:
            c.execute('''
                UPDATE users
                SET age = ?, weight = ?, height = ?, firstname = ?, lastname = ?, birth_year = ?, gender = ?
                WHERE username = ?
            ''', (age, weight, height, firstname, lastname, birth_year, gender, username))
        conn.commit()
    except Exception as e:
        print(f"Fehler beim Aktualisieren des Benutzers: {e}")
    finally:
        conn.close()
# Die Funktion update_user macht es möglich, die Benutzerdaten in der Datenbank zu aktualisieren.
# Sie aktualisiert das Alter, das Gewicht, die Größe, das Profilbild, den Vornamen, den Nachnamen, das Geburtsjahr und das Geschlecht des Benutzers.

def get_user_data(username):
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
        SELECT age, weight, height, profile_image, firstname, lastname, birth_year, gender FROM users WHERE username = ?
    ''', (username,))
    user_data = c.fetchone()
    conn.close()
    return user_data
# Die Funktion get_user_data(username) gibt die Benutzerdaten für einen bestimmten Benutzernamen zurück.

def get_user_age(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT age FROM users WHERE username=?", (username,))
    age = cursor.fetchone()
    conn.close()
    if age:
        return age[0]
    return None
# Die Funktion get_user_age(username) gibt das Alter eines Benutzers zurück, der in der Datenbank gespeichert ist.

def get_user_weight(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT weight FROM users WHERE username=?", (username,))
    weight = cursor.fetchone()
    conn.close()
    if weight:
        return weight[0]
    return None
# Die Funktion get_user_weight(username) gibt das Gewicht eines Benutzers zurück, der in der Datenbank gespeichert ist.

def get_user_height(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT height FROM users WHERE username=?", (username,))
    height = cursor.fetchone()
    conn.close()
    if height:
        return height[0]
    return None
# Die Funktion get_user_height(username) gibt die Größe eines Benutzers zurück, der in der Datenbank gespeichert ist.

def add_user_file(user_id, file_path):
    try:
        conn = create_connection()
        c = conn.cursor()
        c.execute('''
            INSERT INTO user_files (user_id, file_path)
            VALUES (?, ?)
        ''', (user_id, file_path))
        conn.commit()
    except Exception as e:
        print(f"Fehler beim Hinzufügen der Datei: {e}")
    finally:
        conn.close()
# Die Funktion add_user_file(user_id, file_path) fügt den Dateipfad einer Datei hinzu, die einem Benutzer zugeordnet ist.
# Sie fügt den Benutzer-ID und den Dateipfad in die Tabelle 'user_files' ein.

def get_user_files(user_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
        SELECT file_path FROM user_files WHERE user_id = ?
    ''', (user_id,))
    files = c.fetchall()
    conn.close()
    return [file[0] for file in files]
# Die Funktion get_user_files(user_id) gibt die Dateipfade der Dateien zurück, die einem bestimmten Benutzer zugeordnet sind.

# Initialisierung der Datenbank
init_db()
