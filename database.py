import streamlit as st
import pandas as pd
import sqlite3

def create_connection():
    conn = sqlite3.connect('data.db')
    return conn

def init_db():
    conn = create_connection()
    c = conn.cursor()
    # Check if 'profile_image', 'firstname', 'lastname', 'birth_year', 'gender' columns exist and add them if they don't
    c.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in c.fetchall()]
    if 'profile_image' not in columns:
        c.execute('''
            ALTER TABLE users ADD COLUMN profile_image BLOB
        ''')
    if 'firstname' not in columns:
        c.execute('''
            ALTER TABLE users ADD COLUMN firstname TEXT
        ''')
    if 'lastname' not in columns:
        c.execute('''
            ALTER TABLE users ADD COLUMN lastname TEXT
        ''')
    if 'birth_year' not in columns:
        c.execute('''
            ALTER TABLE users ADD COLUMN birth_year INTEGER
        ''')
    if 'gender' not in columns:
        c.execute('''
            ALTER TABLE users ADD COLUMN gender TEXT
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

def get_user(username):
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
        SELECT * FROM users WHERE username = ?
    ''', (username,))
    user = c.fetchone()
    conn.close()
    return user

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

def get_user_data(username):
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
        SELECT age, weight, height, profile_image, firstname, lastname, birth_year, gender FROM users WHERE username = ?
    ''', (username,))
    user_data = c.fetchone()
    conn.close()
    return user_data

def get_user_age(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT age FROM users WHERE username=?", (username,))
    age = cursor.fetchone()
    conn.close()
    if age:
        return age[0]
    return None

def get_user_weight(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT weight FROM users WHERE username=?", (username,))
    weight = cursor.fetchone()
    conn.close()
    if weight:
        return weight[0]
    return None

def get_user_height(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT height FROM users WHERE username=?", (username,))
    height = cursor.fetchone()
    conn.close()
    if height:
        return height[0]
    return None

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

def get_user_files(user_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
        SELECT file_path FROM user_files WHERE user_id = ?
    ''', (user_id,))
    files = c.fetchall()
    conn.close()
    return [file[0] for file in files]
