import base64

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from src.pbkdf2_hasher import Pdkdf2Hasher


class AESCipher(object):
    def __init__(self):
        self.bs = AES.block_size

    def encrypt(self, raw: str, key: str) -> str:
        raw = pad(raw.encode(), AES.block_size)
        iv = Random.new().read(AES.block_size)
        hash_key = Pdkdf2Hasher.hash(key, iv)
        cipher = AES.new(hash_key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw)).decode()

    def decrypt(self, enc: str, key: str) -> str:
        enc = base64.b64decode(enc)
        iv = enc[: AES.block_size]
        hash_key = Pdkdf2Hasher.hash(key, iv)
        cipher = AES.new(hash_key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[AES.block_size :]), AES.block_size).decode(
            "utf-8"
        )
