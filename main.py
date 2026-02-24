import base64
import time
import json
import requests
from urllib.parse import quote
from Crypto.Cipher import DES3 #pip install pycryptodome
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.py3compat import bchr, bord
import warnings

ECID_HEX = "0000000000000000"
Model = "iPhone4,1"

def encrypt3DES(data, key):
    try:
        key_bytes = key.encode('utf-8') if isinstance(key, str) else key
        if len(key_bytes) > 24:
            key_bytes = key_bytes[:24]
        elif len(key_bytes) < 24:
            repeat_count = (24 + len(key_bytes) - 1) // len(key_bytes)
            key_bytes = (key_bytes * repeat_count)[:24]
        data_bytes = data.encode('utf-8') if isinstance(data, str) else data
        block_size = 8
        padding_len = block_size - (len(data_bytes) % block_size)
        padded_data = data_bytes + bytes([padding_len]) * padding_len
        cipher = DES3.new(key_bytes, DES3.MODE_ECB)
        encrypted = cipher.encrypt(padded_data)
        return base64.b64encode(encrypted).decode('utf-8')
    except Exception as e:
        print(f"Encryption error: {e}")
        return False

if __name__ == "__main__":
    ECID_DEC = int(ECID_HEX,16)
    encrypt_data = {
        'ecid': ECID_DEC,
        'model': Model,
        'time': int(round(time.time() * 1000))
    }
    json_data = json.dumps(encrypt_data)
    key = '2015aisi1234sj7890smartflashi4pc'
    encrypted_param = encrypt3DES(data=json_data,key=key)
    encoded_param = quote(encrypted_param,safe='')
    url = "https://i4tool2.i4.cn/requestBackupSHSHList.xhtml?param=" + encoded_param
    Response = requests.get(url)
    data = json.loads(Response.text)
    ios_ver = [item["ios"] for item in data["list"]]
    print(ios_ver)