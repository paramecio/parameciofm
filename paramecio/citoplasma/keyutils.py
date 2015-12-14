from hashlib import sha512
from os import urandom

def create_key_encrypt(n=10):
    
    return sha512(urandom(n)).hexdigest()
