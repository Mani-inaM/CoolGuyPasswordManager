import os
import hashlib
import json
import random
import string

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

class Helper:
    def __init__(self, base_dir=None):
        # Base directory relative to the source folder
        if base_dir is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))  # Use the current directory of the script

        # Setting relative paths to the "data" folder inside the base_dir
        data_dir = os.path.join(base_dir, 'data')

        # Ensure the "data" folder exists
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        self.salt_file = os.path.join(data_dir, 'salt.salt')
        self.key_file = os.path.join(data_dir, 'kek.key')
        self.master_password_file = os.path.join(data_dir, 'master_password.json')

        self.salt = self.load_salt()
        self.kek = self.load_key()

    def load_salt(self):
        return self.load_file(self.salt_file, os.urandom(16))

    def load_key(self):
        return self.load_file(self.key_file, os.urandom(32))

    def load_file(self, file_path, default_data):
        if not os.path.exists(file_path):
            # If the file doesn't exist, create it with default_data
            with open(file_path, 'wb') as f:
                f.write(default_data)
        with open(file_path, 'rb') as f:
            return f.read()

    def derive_key(self, password):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
            backend=default_backend()
        )
        return kdf.derive(password.encode())

    def hash_password(self, password):
        return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), self.salt, 100000)

    def verify_hashed_password(self, hashed_password, provided_password):
        return self.hash_password(provided_password) == hashed_password

    def verify_master_password(self, provided_password):
        # Check if the master password file exists
        if not os.path.exists(self.master_password_file):
            raise ValueError("Master password file does not exist. Please create a new user.")

        with open(self.master_password_file, 'r') as file:
            stored_data = json.load(file)
            stored_password = bytes.fromhex(stored_data['master_password'])
            return self.verify_hashed_password(stored_password, provided_password)

    def store_master_password(self, master_password):
        hashed_password = self.hash_password(master_password)
        with open(self.master_password_file, 'w') as file:
            json.dump({'master_password': hashed_password.hex()}, file)

    def generate_password(self, length=12):
        """Generate a random password of given length"""
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for i in range(length))
        return password
