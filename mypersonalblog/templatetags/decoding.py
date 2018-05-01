import base64
import os
from hashlib import sha256
from hmac import HMAC


def encrypt_password(password, salt=None):
    """
    密码加密方法
    :param password: 密码
    :param salt: 自定义8位随机数
    :return:
    """
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
    """
    利用base64将密码解码
    :param hashed:
    :return:
    """
    pwd = base64.b64encode(hashed)
    return pwd.decode('utf-8')


def enc(hashed):
    """
    利用base64将密码加密
    :param hashed:
    :return:
    """
    return base64.b64decode(hashed)


def validate_password(hashed, password):
    """
    将登陆输入的密码利用注册时的8位随机码加密，验证是否一致
    完成登陆验证
    :param hashed: 加密后的密码
    :param password: 登陆时输入的密码
    :return:
    """
    rehashed = encrypt_password(password, salt=hashed[:8])
    return hashed == rehashed

