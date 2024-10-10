# CoolGuyPasswordManager

## Project Overview

This project is a simple password manager that allows users to store and manage their credentials securely on a single device. The password manager offers functionality for generating strong passwords and retrieving stored credentials, with a focus on security and usability.

## Features

- **Secure Local Storage**: Credentials are securely stored in a local SQLite database using AES encryption.
- **Master Password**: The application requires a master password to access stored credentials.
- **Password Generation**: A built-in password generator helps users create strong, random passwords.
- **User-Friendly Interface**: The application provides a graphical interface built with Tkinter to make it easy to store and retrieve passwords.

## Security Model

The password manager uses a combination of encryption and hashing techniques to ensure that user data is stored securely.

### Key Components

1. **Master Password Protection**:
   - The master password is hashed using PBKDF2 with a SHA-256 hashing algorithm and a unique salt for each user.
   - The hashed master password is stored in a JSON file and compared with the user's input to verify authenticity.

2. **AES Encryption**:
   - All stored passwords are encrypted using AES (Advanced Encryption Standard) with GCM mode to ensure confidentiality and integrity.
   - A 256-bit encryption key is derived using PBKDF2 from the master password.
   - Each stored password is encrypted with a unique initialization vector (IV) to prevent encryption pattern analysis.

3. **Password Generation**:
   - The password generator creates random passwords using a combination of letters, numbers, and special characters.
   - The generated password length is customizable, with a default length of 12 characters for strong password security.

4. **Local Database**:
   - SQLite is used to store the encrypted credentials locally. The database itself does not contain unencrypted data, and all sensitive information is encrypted before insertion.
   - The database schema is designed with simplicity in mind, focusing on secure storage and retrieval.

### Cryptographic Decisions

- **Hashing Algorithm**: PBKDF2 with SHA-256 is chosen due to its resistance to brute-force attacks, with 100,000 iterations for key stretching to make password guessing more difficult.
- **Encryption**: AES-GCM is selected for encryption due to its robustness in providing both confidentiality and integrity. GCM mode ensures that any tampering with the encrypted data can be detected.

### Threat Model

- **Protected Against**:
  - Unauthorized access: Only users who know the master password can decrypt and access the stored credentials.
  - Data exposure: All passwords are stored in an encrypted format, minimizing the risk of data exposure in case the database is compromised.

- **Limitations**:
  - Physical device access: If an attacker gains physical access to the device and master password, the credentials could be exposed. However, strong master passwords and secure device practices are recommended to mitigate this.
  - Master password compromise: The security of all stored credentials relies on the strength and secrecy of the master password.


**Potential Pitfalls**

   - Weak Master Password: If the master password is weak, it could be guessed by an attacker, compromising all stored credentials. Users are advised to choose strong, unique master passwords.
   - Physical Device Security: Since the passwords are stored locally, physical access to the device increases the risk of data theft. Users should ensure their device is protected by operating system-level security measures.
## Setup Instructions

### Prerequisites

- Python 3.x
- The following Python libraries are required:
  - `tkinter`
  - `cryptography`
  - `sqlite3`

### Installation Steps

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
