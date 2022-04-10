import bcrypt, os, hashlib, hmac
from uuid import uuid4


def bhash_value(value):
    value = value.encode()
    hashed = bcrypt.hashpw(value, bcrypt.gensalt(12))
    return hashed.decode()


def bcheck_hash(value, hash):
    res = bcrypt.checkpw(value.encode(), hash.encode())
    return res


def hashed_token():
    value = uuid4().hex
    secret = os.environ["HASH_SECRET"]
    enc_token = hmac.new(secret.encode(), value.encode(), hashlib.sha256).hexdigest()
    return enc_token


def hash_value(value):
    secret = os.environ["HASH_SECRET"]
    enc_token = hmac.new(secret.encode(), value.encode(), hashlib.sha256).hexdigest()
    return enc_token