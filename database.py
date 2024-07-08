import streamlit as st
import pandas as pd
import sqlite3

# Database functions
def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            email TEXT,
            name TEXT,
            age INTEGER,
            weight REAL,
            height REAL
        )
    ''')
    conn.commit()
    conn.close()

def register_user(username, password, email, name):
    try:
        conn = sqlite3.connect('data.db')
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
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        SELECT * FROM users WHERE username = ?
    ''', (username,))
    user = c.fetchone()
    conn.close()
    return user

def update_user(username, age, weight, height, password):
    try:
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute('''
            UPDATE users
            SET age = ?, weight = ?, height = ?, password = ?
            WHERE username = ?
        ''', (age, weight, height, password, username))
        conn.commit()
    except Exception as e:
        print(f"Fehler beim Aktualisieren des Benutzers: {e}")
    finally:
        conn.close()

def get_user_data(username):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        SELECT age, weight, height, password FROM users WHERE username = ?
    ''', (username,))
    user_data = c.fetchone()
    conn.close()
    return user_data