from hashlib import pbkdf2_hmac
import os


class Pdkdf2Hasher:
    iterations = 100000
    salt = os.urandom(16)
    dklen = 32
    hash_name = "sha256"

    @staticmethod
    def hash(string: str, salt: bytes) -> str:
        return pbkdf2_hmac(
            Pdkdf2Hasher.hash_name,
            string.encode(),
            salt,
            Pdkdf2Hasher.iterations,
            Pdkdf2Hasher.dklen,
        )
