from helper import Helper
from encryption_manager import EncryptionManager
from database_manager import DatabaseManager


class PasswordManager:
    def __init__(self):
        # Base directory is automatically set relative to the source folder
        base_dir = None
        self.helper = Helper(base_dir=base_dir)
        self.db = DatabaseManager(base_dir=base_dir)
        self.encryption_manager = EncryptionManager(self.helper.kek)

    def verify_master_password(self, provided_password):
        return self.helper.verify_master_password(provided_password)

    def create_user(self, master_password):
        self.helper.store_master_password(master_password)

    def retrieve_all_services(self, master_password):
        if self.verify_master_password(master_password):
            services = {}
            rows = self.db.retrieve_all_services()
            for row in rows:
                service, username, enc_password = row
                password = self.encryption_manager.decrypt_data(enc_password).decode()
                services[service] = (username, password)
            return services
        return None

    def store_password(self, service, username, password):
        encrypted_password = self.encryption_manager.encrypt_data(password)
        self.db.store_password(service, username, encrypted_password)