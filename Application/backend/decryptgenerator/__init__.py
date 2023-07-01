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

def decrypt(encrypted, key):
    try:
        decrypted = decrypt_3des(encrypted, key)
        return decrypted.decode('utf-8')

    except:
        pass

def ucddecrypt(encrypted, key):
    try:
        decrypted = decrypt_3des(encrypted, key)
        decryptediki = decrypt_3des(eval(str((decrypted))), key)
        decrypteduc = decrypt_3des(eval(str((decryptediki))), key)
        return decrypteduc.decode('utf-8')
    except:
        pass