import requests, base64, os, io
from json import dumps, loads

from osuosu import workspace, localAddr
from osuosu import localPort, infoCache, listJson
from sharep import mkdir, baseEqualPadding, decode
from sharep import writeJson, createWeight

#这里只提供行为逻辑判断
def burst(infoCacheDict):
    #提示输入相关信息
    if len(infoCacheDict['sub_url']) <= 0:
        infoCacheDict['sub_url'] = input('Input subscription url:')
    if len(infoCacheDict['save_folder']) <= 0:
        infoCacheDict['save_folder'] = input('Input config save folder:')
    #检查目录
    mkdir(infoCacheDict['save_folder'])

    res = requests.get(infoCacheDict['sub_url']).content
    ssrCodeList = base64.b64decode(baseEqualPadding(res)).decode('utf-8').replace('\n','').split('ssr://')

    domainList = ''
    portList = ''
    ssrList = {}

    #对数据的解析
    for ssrItem in ssrCodeList:
        if len(ssrItem) <= 0:
            continue
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

        ssrDict['local_address'] = localAddr
        ssrDict['local_port'] = localPort
        ssrDict['fast_open'] = False
        ssrDict['workers'] = 1

        fileName = ssssss[0]
        domainList += ssssss[0] + ' '
        if ssssss[1] not in portList:
            portList += ssssss[1] + ' '
        
        writeJson('{}.json'.format(fileName), ssrDict, infoCacheDict['save_folder'])

        ssrList[fileName] = ssrDict['remarks']

    infoCacheDict['server'] = domainList.strip()
    infoCacheDict['port'] = portList.strip().replace(' ',',')
    #写缓存
    createWeight(ssrList)
    writeJson(listJson, ssrList, infoCacheDict['save_folder'])
    writeJson(infoCache,infoCacheDict)