import base64
import os
from hashlib import sha256
from hmac import HMAC


def encrypt_password(password, salt=None):
    if salt is None:
        salt = os.urandom(8)  # 64 bits.

    assert 8 == len(salt)

    if isinstance(password, str):
        password = password.encode('UTF-8')

    result = password
    for i in range(10):
        result = HMAC(result, salt, sha256).digest()
        hashed = salt + result
    return hashed


def dec(hashed):
    pwd = base64.b64encode(hashed)
    return pwd.decode('utf-8')


def enc(hashed):
    return base64.b64decode(hashed)


def validate_password(hashed, password):
    rehashed = encrypt_password(password, salt=hashed[:8])
    return hashed == rehashed
