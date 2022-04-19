import requests
import os
import sqlite3
import base64
import json
from win32crypt import CryptUnprotectData
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def getstring(local_state):
    with open(local_state, 'r', encoding='utf-8') as f:
        s = json.load(f)['os_crypt']['encrypted_key']
    return s


def pullthekey(base64_encrypted_key):
    encrypted_key_with_header = base64.b64decode(base64_encrypted_key)
    encrypted_key = encrypted_key_with_header[5:]
    key = CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    return key


def decryptstring(key, data):
    nonce, cipherbytes = data[3:15], data[15:]
    aesgcm = AESGCM(key)
    plainbytes = aesgcm.decrypt(nonce, cipherbytes, None)
    plaintext = plainbytes.decode('utf-8')
    return plaintext


def getcookiefromchrome(host):
    local_state = os.environ['LOCALAPPDATA'] + \
        r'/Google/Chrome/User Data/Local State'
    cookie_path = os.environ['LOCALAPPDATA'] + \
        r"/Google/Chrome/User Data/Default/Network/Cookies"

    sql = "select host_key,name,encrypted_value from cookies where host_key='%s'" % host

    with sqlite3.connect(cookie_path) as conn:
        conn.text_factory = bytes
        cu = conn.cursor()
        res = cu.execute(sql).fetchall()
        cu.close()
        cookies = {}
        key = pullthekey(getstring(local_state))
        for _, name, encrypted_value in res:
            if encrypted_value[0:3] == b'v10':
                cookies[name] = decryptstring(key, encrypted_value)
            else:
                cookies[name] = CryptUnprotectData(encrypted_value)[1].decode()
        return cookies


def initsession():
    print("init session")
    baseheaders = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
                   'Accept-Encoding': 'gzip, deflate, br',
                   'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'}
    s = requests.Session()
    cookiedict = getcookiefromchrome('.pixiv.net')
    cookiestr = ""
    for key, value in cookiedict.items():
        cookiestr += "{0}={1}; ".format(str(key, 'utf-8'), value)
    baseheaders['Cookie'] = cookiestr
    s.headers = baseheaders
    s.cookies = requests.utils.cookiejar_from_dict(
        cookiedict, cookiejar=None, overwrite=True)

    try:
        code = s.get('https://www.pixiv.net/ajax/user/extra',
                     allow_redirects=False).status_code

        if code == 200:
            print("access 200.")
            return s, baseheaders
        else:
            raise Exception(
                "You need to login to Pixiv on Chrome or check your internet. code:{0}".format(code))
    except Exception as e:
        print(e)
        raise Exception("Request error.")
