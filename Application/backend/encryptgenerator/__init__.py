from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

# Generate a key
key = b'\x99' * 24


def encrypt_3des(message, key):
    # Generate an IV (Initialization Vector)
    iv = b'\x99' * 8  # Replace with a secure IV

    # Pad the message
    padder = padding.PKCS7(64).padder()
    padded_data = padder.update(message) + padder.finalize()

    # Create the cipher
    cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv), backend=default_backend())

    # Encrypt the data
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    return encrypted_data


def decrypt_3des(encrypted_data, key):
    # Generate an IV (Initialization Vector)
    iv = b'\x99' * 8  # Replace with the same IV used for encryption

    # Create the cipher
    cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv), backend=default_backend())

    # Decrypt the data
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Unpad the decrypted data
    unpadder = padding.PKCS7(64).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

    return unpadded_data


def encrypt(str, key):
    encrypted = encrypt_3des(str.encode('utf-8'), key)
    return encrypted

def ucdencrypt(str, key):
    encrypted = encrypt_3des(str.encode('utf-8'), key)
    encryptediki = encrypt_3des(encrypted, key)
    encrypteduc = encrypt_3des(encryptediki, key)
    return encrypteduc