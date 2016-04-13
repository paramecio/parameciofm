from hashlib import sha512, sha256
from base64 import b64encode
from os import urandom

def create_key_encrypt(n=10):
    
    return sha512(urandom(n)).hexdigest()

def create_key_encrypt_256(n=10):
    
    return sha256(urandom(n)).hexdigest()

def create_key(n=10):
    
    rand_bytes=urandom(n)
    
    return b64encode(rand_bytes).decode('utf-8')
