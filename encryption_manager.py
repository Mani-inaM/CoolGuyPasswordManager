from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import os


class EncryptionManager:
    def __init__(self, key):
        self.key = key

    def encrypt_data(self, data):
        iv = os.urandom(12)  # IV should be unique for each encryption
        encryptor = Cipher(
            algorithms.AES(self.key),
            modes.GCM(iv),
            backend=default_backend()
        ).encryptor()
        ciphertext = encryptor.update(data.encode()) + encryptor.finalize()
        return base64.b64encode(iv + ciphertext + encryptor.tag).decode()

    def decrypt_data(self, enc_data):
        enc_data = base64.b64decode(enc_data.encode())
        iv = enc_data[:12]
        tag = enc_data[-16:]
        ciphertext = enc_data[12:-16]
        decryptor = Cipher(
            algorithms.AES(self.key),
            modes.GCM(iv, tag),
            backend=default_backend()
        ).decryptor()
        return decryptor.update(ciphertext) + decryptor.finalize()