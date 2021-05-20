import hashlib

from django.conf import settings


def md5(str):
    """对密码进行MD5加密"""
    # 使用本地的django-secret-key进行加盐
    hash_obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    hash_obj.update(str.encode('utf-8'))
    return hash_obj.hexdigest()