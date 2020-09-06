# pip install passlib
from passlib.context import CryptContext

pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000 ## TODO: edit the number of rounds
)

'''
argument: password text
returns: encrypted password
'''
def encrypt_password(password):
    return pwd_context.encrypt(password)

'''
argument: password text, encrypted password from encrypt_password(password) method
returns: True if passwords match
'''
def check_encrypted_password(password, hashed):
    return pwd_context.verify(password, hashed)
