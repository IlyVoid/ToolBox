# 🦫 Password Manager Script by 𝖇𝖑4𝖘𝖘
# GitHub: https://github.com/IlyVoid

import os
import json
from cryptography.fernet import Fernet
from getpass import getpass

# Generate a key for encryption/decryption (this should be saved securely)
def generate_key():
    return Fernet.generate_key()

# Save the key to a file (never expose this key)
def save_key(key, filename="secret.key"):
    with open(filename, "wb") as key_file:
        key_file.write(key)

# Load the encryption key
def load_key(filename="secret.key"):
    return open(filename, "rb").read()

# Encrypt the password
def encrypt_password(password, key):
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password

# Decrypt the password
def decrypt_password(encrypted_password, key):
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_password).decode()
    return decrypted_password

# Save the passwords to a file (JSON format)
def save_password_to_file(service, encrypted_password, filename="passwords.json"):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            passwords = json.load(file)
    else:
        passwords = {}

    passwords[service] = encrypted_password
    with open(filename, "w") as file:
        json.dump(passwords, file, indent=4)

# Retrieve the password from the file
def retrieve_password(service, key, filename="passwords.json"):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            passwords = json.load(file)

        if service in passwords:
            encrypted_password = passwords[service]
            return decrypt_password(encrypted_password, key)
        else:
            print(f"Service {service} not found.")
            return None
    else:
        print(f"No password file found.")
        return None

# Main function
def main():
    print("🦫 Welcome to ProtectiveBeaver")
    
    # Ask for the encryption key or generate a new one
    if not os.path.exists("secret.key"):
        print("No encryption key found. Generating a new one...")
        key = generate_key()
        save_key(key)
    else:
        key = load_key()
    
    # Main Menu
    while True:
        print("\n1. Store a new password")
        print("2. Retrieve a password")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            service = input("Enter the service (e.g., Gmail, GitHub): ")
            password = getpass("Enter the password to store: ")
            encrypted_password = encrypt_password(password, key)
            save_password_to_file(service, encrypted_password)
            print(f"Password for {service} has been securely stored.")

        elif choice == "2":
            service = input("Enter the service to retrieve the password: ")
            retrieved_password = retrieve_password(service, key)
            if retrieved_password:
                print(f"Password for {service}: {retrieved_password}")

        elif choice == "3":
            print("Exiting Password Manager...")
            break

        else:
            print("Invalid choice. Please try again.")

# Run the password manager
if __name__ == "__main__":
    main()
