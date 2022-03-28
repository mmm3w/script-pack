import requests
import os
import sqlite3
import json
import base64
import win32crypt
from win32crypt import CryptUnprotectData
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

baseFolder = os.path.split(os.path.realpath(__file__))[0] 
testUrl = 'https://www.pixiv.net/ajax/user/extra'
profileUrl = 'https://www.pixiv.net/ajax/user/{0}/profile/all?lang=zh'
artworksUrl = 'https://www.pixiv.net/artworks/{0}'
pageUrl = 'https://www.pixiv.net/ajax/illust/{0}/pages?lang=zh'
baseHeaders = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}

def getString(local_state):
    with open(local_state, 'r', encoding='utf-8') as f:
        s = json.load(f)['os_crypt']['encrypted_key']
    return s

def pullTheKey(base64_encrypted_key):
    encrypted_key_with_header = base64.b64decode(base64_encrypted_key)
    encrypted_key = encrypted_key_with_header[5:]
    key = CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    return key

def decryptString(key, data):
    nonce, cipherbytes = data[3:15], data[15:]
    aesgcm = AESGCM(key)
    plainbytes = aesgcm.decrypt(nonce, cipherbytes, None)
    plaintext = plainbytes.decode('utf-8')
    return plaintext

def getCookieFromChrome(host):
    local_state = os.environ['LOCALAPPDATA'] + r'\Google\Chrome\User Data\Local State'
    cookie_path = os.environ['LOCALAPPDATA'] + r"\Google\Chrome\User Data\Default\Cookies"
    
    sql = "select host_key,name,encrypted_value from cookies where host_key='%s'" % host

    with sqlite3.connect(cookie_path) as conn:
        cu = conn.cursor()
        res = cu.execute(sql).fetchall()
        cu.close()
        cookies = {}
        key = pullTheKey(getString(local_state))
        for host_key, name, encrypted_value in res:
            if encrypted_value[0:3] == b'v10':
                cookies[name] = decryptString(key, encrypted_value)
            else:
                cookies[name] = CryptUnprotectData(encrypted_value)[1].decode()
        # print(cookies)
        return cookies

def initSession(h):
    print("Init session")
    s = requests.Session()
    s.headers = h
    s.cookies = requests.utils.cookiejar_from_dict(getCookieFromChrome('.pixiv.net'), cookiejar=None, overwrite=True)
    return s

def chechLogin(session, u):
    code = session.get(u, allow_redirects=False).status_code
    if code == 200:
        print("Checked. code:{0}".format(code))
        return True
    else:
        print("You need to login to Pixiv on Chrome or check your internet. code:{0}".format(code))
        return False

def downloadFile(session, download_url, local_path):
    local_filename = download_url.split('/')[-1]
    wait_path = os.path.join(local_path, "waiting_" + local_filename)
    save_path = os.path.join(local_path, local_filename)

    if os.path.exists(save_path):
        print('[Skip]{} already exists.'.format(save_path))
        return save_path

    try:
        r = session.get(download_url, stream=True)
        if r.status_code != 200:
            print("Download Fail. Code:{0}".format(r.status_code))
            return ""
    except:
        return ""
        
    size = 0
    total_size = int(r.headers.get('content-length', 0))
    if total_size >= 1024:
        chunk_size = 1024
        unit = "KB"
    else:
        chunk_size = 1
        unit = "Byte"
    print("Download File : " + download_url)
    print("Total size : {0:.2f}{1}".format(float(total_size / chunk_size), unit))

    if os.path.exists(wait_path):
        if total_size == os.path.getsize(wait_path):
            os.rename(wait_path, save_path)
            print('[Skip]{} check over.'.format(save_path))
            return save_path

    with open(wait_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size):
            if chunk:
                f.write(chunk)
                size += len(chunk)
                print(("\rDownloading [{1}] {0:.2f}%") \
                .format( float(size / total_size * 100), \
                '>' * int(size * 50 / total_size) + '=' * (50 - int(size * 50 / total_size))) , end='')
    
    if total_size == os.path.getsize(wait_path):
            os.rename(wait_path, save_path)
    print()
    return save_path

def getIllustsList(session, url):
    result = session.get(url).json()
    illusts = []
    for key, value in result['body']['illusts'].items():
        illusts.append(key)
    print("Total:{0}".format(len(illusts)))
    return illusts

#illustsID 单个图片pid
def downloadArtworks(session, illustsID):
    try:
        del baseHeaders['Referer']
    except:
        pass
    session.headers = baseHeaders
    result = session.get(pageUrl.format(illustsID)).json()
    for item in result['body']:
        baseHeaders['Referer'] = artworksUrl.format(illustsID)
        session.headers = baseHeaders
        downloadFile(session, item['urls']['original'], baseFolder)

#userID 作者的id
def traverseCreator(session, userID):
    global baseFolder, profileUrl, baseHeaders
    illustsList =  getIllustsList(session, profileUrl.format(userID))
    for illusts in illustsList:
        downloadArtworks(session, illusts)

session = initSession(baseHeaders)
chechLogin(session, testUrl)
id = input("Input pixiv user id:")
traverseCreator(session, id)
input('Finish!')