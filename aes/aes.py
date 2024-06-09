from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import scrypt


def encrypt_data(data, password):
    salt = get_random_bytes(16)
    key = scrypt(password, salt, key_len=32, N=2**14, r=8, p=1)
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode('utf-8'))
    return salt + cipher.nonce + tag + ciphertext


def decrypt_data(encrypted_data, password):
    salt = encrypted_data[:16]
    nonce = encrypted_data[16:32]
    tag = encrypted_data[32:48]
    ciphertext = encrypted_data[48:]
    key = scrypt(password, salt, key_len=32, N=2**14, r=8, p=1)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
    return decrypted_data.decode('utf-8')


SECRET_KEY = "c04022286c7adb7f910b82675cad956574acd1bad60fa4edd653225453929b83"
