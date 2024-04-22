from Crypto.Cipher import AES
import base64
import os
import hashlib
import time


def generate_uuid():
    current_time = str(time.time()).encode('utf-8')
    random_bytes = os.urandom(16)
    mix = current_time + random_bytes
    hashed_uuid = hashlib.sha1(mix).hexdigest()
    return f"{hashed_uuid[:8]}-{hashed_uuid[8:12]}-{hashed_uuid[12:16]}-{hashed_uuid[16:20]}-{hashed_uuid[20:32]}"


class Decode:
    def __init__(self, data: str = "", aes_key: str = "zG2nSeEfSHfvTCHy5LCcqtBbQehKNLXn"):
        self.data = data
        self.aes_key = aes_key
        self.iv = b'\0' * 16

    def _pkcs7un_padding(self, data):
        length = len(data)
        un_padding = ord(chr(data[length - 1]))
        return data[0:length - un_padding].decode('utf-8')

    def encrypt(self, text):
        aes_key = hashlib.sha256(self.aes_key.encode('utf-8')).digest()
        aes = AES.new(aes_key, AES.MODE_CBC, self.iv)
        return base64.b64encode(aes.encrypt(text))

    def decrypt(self):
        aes_key = hashlib.sha256(self.aes_key.encode('utf-8')).digest()
        aes = AES.new(aes_key, AES.MODE_CBC, self.iv)
        return self._pkcs7un_padding(aes.decrypt(base64.b64decode(self.data)))
