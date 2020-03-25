import requests, base64, os, io
from json import dumps, loads

def baseEqualPadding(source):
    equalPadding = len(source) % 4
    if equalPadding != 0:
        return source + b'=' * (4 - equalPadding)
    else:
        return source

def repBase(str):
    return str.replace('_','/').replace('-','+')

def decode(str):
    return base64.b64decode(baseEqualPadding(repBase(str).encode())).decode('utf-8')

def checkDirectory(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

confFile = io.open('subscription.json', 'r', encoding='utf-8')
confFileStr = confFile.read()
confFile.close()
confDict = loads(confFileStr)
checkDirectory(confDict['folder'])
checkDirectory(confDict['list'])

ssrList = {}

res = requests.get(confDict['url']).content
ssrCodeList = base64.b64decode(baseEqualPadding(res)).decode('utf-8').replace('\n','').split('ssr://')
for ssrItem in ssrCodeList:
    if len(ssrItem) <= 0:
        continue
    try:
        ssrDict = {}
        ssssss = decode(ssrItem).split(':')
        ssrDict['server'] = ssssss[0]
        ssrDict['server_port'] = int(ssssss[1])
        ssrDict['protocol'] = ssssss[2]
        ssrDict['method'] = ssssss[3]
        ssrDict['obfs'] = ssssss[4]

        ns = ssssss[5].split('/?')
        ssrDict['password'] = decode(ns[0])

        params = ns[1].split('&')
        
        for param in params:
            if param[:param.find('=')] == 'obfsparam':
                ssrDict['obfs_param'] = decode(param[param.find('=') + 1:])
            if param[:param.find('=')] == 'protoparam':
                ssrDict['protocol_param'] = decode(param[param.find('=') + 1:])
            if param[:param.find('=')] == 'remarks':
                ssrDict['remarks'] = decode(param[param.find('=') + 1:])

        ssrDict['local_address'] = '0.0.0.0'
        ssrDict['local_port'] = 60080
        ssrDict['fast_open'] = False
        ssrDict['workers'] = 1

        fileName = ssssss[0][:ssssss[0].find('.')]
        ssrConfigFile = io.open(os.path.join(confDict['folder'], '{}.json'.format(fileName)), 'w', encoding='utf-8')
        ssrConfigFile.write(dumps(ssrDict, ensure_ascii=False))
        ssrConfigFile.close()
        ssrList[fileName] = ssrDict['remarks']
    except:
        pass

sL = io.open(os.path.join(confDict['list'],'ServerList.json'), 'w', encoding='utf-8')
sL.write(dumps(ssrList, ensure_ascii=False))
sL.close()