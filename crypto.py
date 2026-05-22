import os
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

KEY = hashlib.sha256(b"mysharedsecret").digest()
cipher = ChaCha20Poly1305(KEY)

def encrypt(data):
    nonce = os.urandom(12)
    return nonce + cipher.encrypt(nonce, data, None)

def decrypt(data):
    nonce = data[:12]
    return cipher.decrypt(nonce, data[12:], None)
