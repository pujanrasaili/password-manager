import sqlite3
from cryptography.fernet import Fernet
import os

KEY_FILE = 'secret.key'

def generate_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as f:
            f.write(key)

def load_key():
    return open(KEY_FILE, 'rb').read()

def encrypt_password(password):
    f = Fernet(load_key())
    return f.encrypt(password.encode()).decode()

def decrypt_password(token):
    f = Fernet(load_key())
    return f.decrypt(token.encode()).decode()

def get_connection():
    conn = sqlite3.connect('passwords.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    generate_key()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            site TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            category TEXT DEFAULT 'General',
            notes TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("Database ready!")

if __name__ == '__main__':
    init_db()