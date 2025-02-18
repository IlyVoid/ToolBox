# 🦫 Password Manager Script by 𝖇𝖑4𝖘𝖘

This is a simple Python-based Password Manager that allows you to securely store and retrieve passwords using encryption.

## Features:
- **Encryption**: Passwords are encrypted using **Fernet** symmetric encryption from the `cryptography` library.
- **Storage**: Passwords are stored in a **JSON** file (`passwords.json`) in encrypted format.
- **Key Management**: An encryption key (`secret.key`) is used to secure and decrypt passwords. This key is generated and saved when running the script.
- **Retrieval**: Retrieve passwords for different services (e.g., Gmail, GitHub) by entering the service name.

## Requirements

To run this script, you need to install the required dependencies.

1. **cryptography**: For encrypting and decrypting passwords.

### Install dependencies:
```bash
pip install -r requirements.txt
```
Usage

    Run the script:
        If no encryption key exists, a new one will be generated and saved as secret.key.
        Choose between storing a new password, retrieving an existing password, or exiting the script.
```bash
python3 ProtectiveBeaver.py
```

    Storing a password:
        Enter the name of the service (e.g., Gmail, GitHub).
        Enter the password you want to store.
        The password will be encrypted and saved.

    Retrieving a password:
        Enter the service name you want to retrieve the password for.
        The corresponding password will be decrypted and displayed.

### Example:
```bash
🦫 Welcome to the Password Manager

1. Store a new password
2. Retrieve a password
3. Exit
Choose an option: 1
Enter the service (e.g., Gmail, GitHub): Gmail
Enter the password to store: ********
Password for Gmail has been securely stored.
```
Security Warning

    Make sure to store the secret.key securely. If the key is lost, the stored passwords cannot be decrypted.
    Do not share the secret.key file, as anyone with access to it can decrypt your passwords.
