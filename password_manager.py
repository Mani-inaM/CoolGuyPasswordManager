from helper import Helper
from encryption_manager import EncryptionManager
from database_manager import DatabaseManager

class PasswordManager:
    def __init__(self):
        base_dir = None
        self.helper = Helper(base_dir=base_dir)
        self.db = DatabaseManager(base_dir=base_dir)

    def verify_master_password(self, provided_password):
        return self.helper.verify_master_password(provided_password)

    def create_user(self, master_password):
        self.helper.store_master_password(master_password)

    def retrieve_all_services(self, master_password):
        if self.verify_master_password(master_password):
            services = {}
            # Derive the encryption key from the provided master password
            encryption_key = self.helper.derive_key(master_password)
            encryption_manager = EncryptionManager(encryption_key)

            rows = self.db.retrieve_all_services()
            for row in rows:
                service, username, enc_password = row
                password = encryption_manager.decrypt_data(enc_password).decode()
                services[service] = (username, password)
            return services
        return None

    def store_password(self, master_password, service, username, password):
        # Derive the encryption key from the provided master password
        encryption_key = self.helper.derive_key(master_password)
        encryption_manager = EncryptionManager(encryption_key)

        encrypted_password = encryption_manager.encrypt_data(password)
        self.db.store_password(service, username, encrypted_password)
