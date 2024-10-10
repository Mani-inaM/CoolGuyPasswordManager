import sqlite3
import os

class DatabaseManager:
    def __init__(self, base_dir=None):
        # Base directory relative to the source folder
        if base_dir is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))  # Use the current directory of the script

        data_dir = os.path.join(base_dir, 'data')
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        self.db_file = os.path.join(data_dir, 'vault.db')
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS passwords (
                    id INTEGER PRIMARY KEY,
                    service TEXT NOT NULL,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL
                )
            ''')
            conn.commit()

    def store_password(self, service, username, encrypted_password):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO passwords (service, username, password)
                VALUES (?, ?, ?)
            ''', (service, username, encrypted_password))
            conn.commit()

    def retrieve_password(self, service):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT username, password FROM passwords WHERE service=?
            ''', (service,))
            row = cursor.fetchone()
        return row

    def retrieve_all_services(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT service, username, password FROM passwords')
            rows = cursor.fetchall()
        return rows