import os
import json
import random
import string
from cryptography.fernet import Fernet

# Function to generate a key for encryption
def generate_key():
    return Fernet.generate_key()

# Function to load or create a key
def load_key():
    if os.path.exists("secret.key"):
        with open("secret.key", "rb") as key_file:
            return key_file.read()
    else:
        key = generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
        return key

# Function to encrypt data
def encrypt_data(data, key):
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data

# Function to decrypt data
def decrypt_data(encrypted_data, key):
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data).decode()
    return decrypted_data

# Function to generate a random password
def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

# Function to save passwords to a file
def save_passwords(passwords, key):
    encrypted_data = encrypt_data(json.dumps(passwords), key)
    with open("passwords.json", "wb") as f:
        f.write(encrypted_data)

# Function to load passwords from a file
def load_passwords(key):
    if not os.path.exists("passwords.json"):
        return {}
    with open("passwords.json", "rb") as f:
        encrypted_data = f.read()
    decrypted_data = decrypt_data(encrypted_data, key)
    return json.loads(decrypted_data)

# Main function to run the password manager
def main():
    key = load_key()
    passwords = load_passwords(key)

    while True:
        print("\nPassword Manager")
        print("1. Add Password")
        print("2. Retrieve Password")
        print("3. Generate Password")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            site = input("Enter the site name: ")
            password = input("Enter the password: ")
            passwords[site] = password
            save_passwords(passwords, key)
            print(f"Password for {site} saved.")

        elif choice == "2":
            site = input("Enter the site name: ")
            if site in passwords:
                print(f"Password for {site}: {passwords[site]}")
            else:
                print("No password found for that site.")

        elif choice == "3":
            site = input("Enter the site name: ")
            length = int(input("Enter the desired password length: "))
            new_password = generate_password(length)
            passwords[site] = new_password
            save_passwords(passwords, key)
            print(f"Generated password for {site}: {new_password}")

        elif choice == "4":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()