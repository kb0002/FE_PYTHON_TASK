import os
from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

def encrypt_video(file_path, key):
    cipher = Fernet(key)
    
    with open(file_path, "rb") as f:
        file_data = f.read()
    
    encrypted_data = cipher.encrypt(file_data)

    encrypted_path = file_path + ".enc"
    with open(encrypted_path, "wb") as f:
        f.write(encrypted_data)

    os.remove(file_path)  # Remove original file
    return encrypted_path

def decrypt_video(file_path, key):
    cipher = Fernet(key)
    
    with open(file_path, "rb") as f:
        encrypted_data = f.read()
    
    return cipher.decrypt(encrypted_data)  # Return decrypted data
