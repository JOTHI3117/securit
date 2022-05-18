from Crypto.Cipher import Blowfish
import Crypto
import os
from django.http import HttpResponse


def pad(s):
    return s + b"\0" * (Blowfish.block_size - len(s) % Blowfish.block_size)


def encrypt(message, key, key_size=256):
    message = pad(message)
    iv = Crypto.Random.new().read(Blowfish.block_size)
    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    print(iv)
    return iv + cipher.encrypt(message)


def decrypt(ciphertext, key):
    iv = ciphertext[:Blowfish.block_size]
    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[Blowfish.block_size:])
    return plaintext.rstrip(b"\0")


def encrypt_file(file_name, key):
    with open(file_name, 'rb') as fo:
        plaintext = fo.read()
    enc = encrypt(plaintext, key)
    with open(file_name, 'wb') as fo:
        fo.write(enc)


def decrypt_file(file_name, key):
    with open(file_name, 'rb') as fo:
        ciphertext = fo.read()
    dec = decrypt(ciphertext, key)
    response = HttpResponse(dec, content_type="application/vnd.ms-excel")
    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_name)
    return response
