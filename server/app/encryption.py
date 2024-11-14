from config import Config

import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def encrypt (raw):
    raw = pad(raw.encode(), 16)
    cipher = AES.new(Config.KEY.encode('utf-8'), AES.MODE_ECB)
    return base64.b64encode(cipher.encrypt(raw))