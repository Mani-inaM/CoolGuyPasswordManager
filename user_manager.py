from helper import Helper

class UserManager:
    def __init__(self, salt_file='salt.salt'):
        self.helper = Helper(salt_file=salt_file)
        self.salt = self.helper.salt

    def hash_password(self, password):
        return self.helper.hash_password(password)

    def verify_password(self, stored_password, provided_password):
        return self.helper.verify_hashed_password(stored_password, provided_password)
