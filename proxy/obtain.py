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


workspace = os.path.split(os.path.realpath(__file__))[0]
subTemp = os.path.join(workspace,'sub.temp')

confFolder = ''
confUrl = ''

#要求输入订阅配置
if os.path.exists(subTemp):
    with io.open(subTemp, 'r', encoding='utf-8') as f:
        confFolder = f.readline().replace('\n', '')
        confUrl = f.readline().replace('\n', '')
else:
    confUrl = input('Input subscription url:')
    confFolder = input('Input config folder:')
    with io.open(subTemp, 'w', encoding='utf-8') as f:
        f.write('{0}\n{1}'.format(confFolder, confUrl))
#检查目录
checkDirectory(confFolder)

ssrList = {}
domainList = ''
portList = ''
#请求数据并解析
res = requests.get(confUrl).content
ssrCodeList = base64.b64decode(baseEqualPadding(res)).decode('utf-8').replace('\n','').split('ssr://')
for ssrItem in ssrCodeList:
    if len(ssrItem) <= 0:
        continue
    try:
        ssrDict = {}
        ssssss = decode(ssrItem).split(':')
        ssrDict['server'] = ssssss[0]
        domainList += ssssss[0] + ' '
        ssrDict['server_port'] = int(ssssss[1])
        if ssssss[1] not in portList:
            portList += ssssss[1] + ' '
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

        with io.open(os.path.join(confFolder, '{}.json'.format(fileName)), 'w', encoding='utf-8') as f:
            f.write(dumps(ssrDict, ensure_ascii=False))
        print('Get {0}:{1} config'.format(ssssss[0], ssssss[1]))

        ssrList[fileName] = ssrDict['remarks']
    except Exception as d:
        print(d)
        pass

#缓存一个服务器列表用于切换服务器
with io.open(os.path.join(confFolder,'list.json'), 'w', encoding='utf-8') as f:
    f.write(dumps(ssrList, ensure_ascii=False))
#缓存域名列表用于修改ss-tproxy配置
with io.open(os.path.join(workspace,'server.temp'), 'w', encoding='utf-8') as f:
    serverDict = {}
    serverDict['server'] = domainList.strip()
    serverDict['port'] = portList.strip().replace(' ',',')
    serverDict['last'] = ''
    f.write(dumps(serverDict, ensure_ascii=False))